# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 15:18:49 2021

@author: Chris Downs

purpose:
    support a library of functions that will allow for the transposition of ghi data (or data from a weather api) to POA data.
    include functions to plot calibration metrics (how well does transposed match actual?) how well does weather api match actual ghi, etc

heiarchy of irradiance data
    1: native functioning POA
    2: neighbor functioning poa from a matching site (within 10 miles, same tilf or gcr, same tracking tech (back vs true))
    3: native site ghi data transposed ot POA (5 MINUTE DATA TRANSPOSED AND RESAMPLED TO HOURLY) dashboard will have an hourly ghi data plot, but transpose on more granular data
    4: neighbor GHI site (doesnt have to match) 5 minute data transposed to poa nd hourly resample
    5: weather API data transposed and resampled to hourly data
"""
import awswrangler as wr
from collections import namedtuple
from re import M
from dateutil import parser
import datetime
import os
import numpy as np
import pandas as pd
from pathlib import Path
import pvlib
from pvlib.location import Location
from multiprocessing.pool import ThreadPool
from typing import NewType

from ccrenew.dashboard import (
    ccr,
    all_df_keys,
    DateLike
)
from ccrenew.dashboard.data_processing import solcats_API as Cats 

df_keys = all_df_keys


def get_weather_data(start: str|DateLike, end: str|DateLike, params: tuple, source: str='satellite',
                     convert: bool = False, pool_size: int=6):
    """
    Query data from AWS to use in irradiance calculations
    
    Args:
        ccr_id (str): CCR ID for the project.
        start (str or DateLike): Start date for the data request.
        end (str or DateLike): Start date for the data request.
        source (str): Option to pull data from satellite recordings or on-site
            measurements. Options: `satellite` or `measured`
        pool_size (int): Number of threads to use when pulling data directly from S3.
    
    Returns
        df_weather (pd.DataFrame): Weather for the project over the specified days.
    """
    def s3_pool(pool_size, keys):
        pool_size = 6
        pool = ThreadPool(pool_size)
        day_df_list = pool.map(Cats.retrieve_df, keys)
        pool.close()
        pool.join()
        
        df_weather = pd.concat(day_df_list, axis=0)
        return df_weather

    date_range = pd.date_range(start, end, normalize=True)

    if source == 'measured':
        keys = [Cats.make_measured_key(params.ccr_id, date) for date in date_range]
        df_weather = s3_pool(pool_size=pool_size, keys=keys)
    else:
        if len(date_range) < 50:
            keys = [Cats.make_satellite_key(params.ccr_id, date) for date in date_range]
            df_weather = s3_pool(pool_size=pool_size, keys=keys)
        else:
            df_weather = wr.athena.read_sql_query(
                sql="""SELECT  local_datetime
                              ,ghi
                              ,dni
                              ,dhi
                              ,air_temp
                              ,wind_speed_10m
                         FROM raw_data
                        WHERE ccr_id=:ccr_id;
                          AND local_datetime>=:CAST(start AS DATE);
                          AND local_datetime<=:CAST(end AS DATE);
                    ORDER BY local_datetime""",
                params={"ccr_id":f"'{params.ccr_id}'",
                        "start":f"{start}",
                        "end":f"{end}"
                        },
                database='solcast'
                )
            df_weather = df_weather.set_index('local_datetime')
    
        if convert:
            # Convert units
            folder = params.folder
            config_file = params.project_name + r'_Plant_Config_MACRO.xlsm'
            config_path = Path(ccr.file_project) / folder / params.project_name / 'Plant_Config_File' / config_file
            xl=pd.ExcelFile(config_path)
            df_config=xl.parse('Unit_Tab')
            
            #temp units
            temps = df_config.loc[df_config['Var_ID'].str.contains('amb')]['Convert_Farenheit_to_Celcius'].sum()
            temps += df_config.loc[df_config['Var_ID'].str.contains('mod')]['Convert_Farenheit_to_Celcius'].sum()
            if temps > 0:
                df_weather['Tamb'] = df_weather['air_temp']*float((9/5.))+32.0
                df_weather['Tmod'] = df_weather['Tmod']*float((9/5.))+32.0
            else:
                df_weather['Tamb'] = df_weather['air_temp']
                
            #wind units
            winds = df_config.loc[df_config['Var_ID'].str.contains('speed')]['Convert_mph_to_mps'].sum()
            if winds > 0:
                df_weather['Wind_speed'] = df_weather['wind_speed_10m']*float(2.23694)
            else:
                df_weather['Wind_speed'] = df_weather['wind_speed_10m']
        else:
            df_weather['Wind_speed'] = df_weather['wind_speed_10m']
            df_weather['Tamb'] = df_weather['air_temp']


    return df_weather

def calculate_poa(df_weather: pd.DataFrame, source: str, params: tuple, resample: bool=True):
    # Infer timeseries frequency & localize timezone to UTC for calcs
    tz_utc = 'UTC'
    freq = pd.infer_freq(df_weather.index)
    df_solcast = df_weather.tz_localize(params.tz, ambiguous=True).tz_convert(tz_utc)

    # Simulate tilt based on racking type (fixed or tracker)
    tilt, surface_azimuth = get_tilt(df_solcast, params)

    # Decompose satellite GHI into DHI & DNI components to use in the `transpose` function below
    components = decompose(df_solcast['ghi'], params.lat, params.lon, params.elevation, tz_utc, freq) 
    ghi, dni, dhi, airmass, dni_et, site_location, solar_position = components

    if source == 'satellite':
        dni = df_solcast['dni']
        dhi = df_solcast['dhi']
    
    # Transpose horizontal irradiance & tilt into POA values
    poa_df = transpose(tilt, surface_azimuth, params.albedo, solar_position, ghi, dni, dhi, dni_et, airmass) 
    df_solcast['poa'] = poa_df['poa_global']

    #do resample
    if resample:
        df_solcast = df_solcast.resample('H').mean()
        df_solcast = df_solcast[~df_solcast.index.duplicated(keep='first')]

    if source == 'satellite':
        #add in a tmod column based on the conversion equation
        a_module = params.a_module
        b_module = params.b_module
        df_solcast['Tmod'] = df_solcast['air_temp']+(df_solcast['poa']*np.exp(a_module+b_module*df_solcast['wind_speed_10m']))

        #correct for static values that solcats reports that the dashboard is gonna turn off.
        df_solcast['Correction_factor'] = np.where(df_solcast.index.hour%2==0, 0.999, 1.001)
        df_solcast['Tamb'] *= df_solcast['Correction_factor']
        df_solcast['Tmod'] *= df_solcast['Correction_factor']
        df_solcast['Wind_speed'] *= df_solcast['Correction_factor']

    df_solcast = df_solcast.tz_convert(params.tz).tz_localize(None)

    return df_solcast

def get_tilt(df_weather: pd.DataFrame, params: tuple):
    #do some cheeky stuff that is racking specific
    if params.racking =='Fixed':
        surface_azimuth = 180
        
        #make even fixed tilts a df of values so every time slot has a value and tz localize works the same for fixed vs trackers
        df_index = df_weather.index
        tracker_data = pd.DataFrame(index=df_index, data={'surface_tilt': params.tilt_gcr,
                                                          'surface_azimuth': surface_azimuth})
    elif params.racking =='Tracker':
        tracker_data = simulate_trackers(df_weather, params)

    surface_azimuth = tracker_data['surface_azimuth']
    tilt = tracker_data['surface_tilt']

    return tilt, surface_azimuth

def simulate_trackers(df_weather, params):
   
    #choose tracking algorithm based upon temp_coefficient of the modules
    backtrack=True
    if params.temp_coef > -0.39:
        backtrack=False
  
    # altitude in meters above sea level.  name is optional, but helpful for documentation
    site_location = Location(params.lat, params.lon, altitude=params.elevation, tz=params.tz)
     
    solar_position = site_location.get_solarposition(df_weather.index, params.lat, params.lon)
    
    tracker_data = pvlib.tracking.singleaxis(solar_position['apparent_zenith'], solar_position['azimuth'],
                                             axis_tilt=params.axis_tilt, axis_azimuth=params.axis_azimuth,
                                             max_angle=params.max_angle, backtrack=backtrack, gcr=params.tilt_gcr)
    
    return tracker_data

def decompose(ghi, lat, lon, elevation, tz, freq):
    """
    decompose the given ghi dataframe into both dhi and dni
    
    Parameters
    ----------
    df: pandas df of ghi data
    lat: Numeric. site latitude as a decimal
    lon: Numeric. site longitude as a decimal
    
    Returns
    -------
    dni
    dhi
    airmass
    dni_et
    """
    site_location = Location(lat, lon, tz=tz, altitude=elevation)
    solar_position = site_location.get_solarposition(times=ghi.index)
    dni_et = pvlib.irradiance.get_extra_radiation(ghi.index)
    airmass = site_location.get_airmass(solar_position=solar_position)['airmass_relative']
    zenith = solar_position.apparent_zenith
    erb = pvlib.irradiance.erbs(ghi, zenith, ghi.index)
    dni = erb['dni']
    dhi = erb['dhi']
    
    return ghi, dni, dhi, airmass, dni_et, site_location, solar_position

def transpose(surface_tilt, surface_azimuth, albedo, solar_position,
              ghi, dni, dhi, dni_et, airmass, **kwargs):
    """
    Estimate POA irradiance. PVWatts v5 uses a similar but slightly different
    method for near-horizon diffuse irradiance.

    Parameters
    ----------
    surface_tilt, surface_azimuth : numeric
        Array orientation [degrees]
    albedo : numeric
        Ground albedo
    solar_position : pd.DataFrame
        Solar position
    ghi, dni, dhi : numeric
        The three irradiance components
    airmass : numeric
        relative airmass
    dni_et : numeric
        extraterrestrial (top of atmosphere) irradiance
    **kwargs
        Extra arguments passed to ``pvlib.irradiance.get_total_irradiance``.

    Returns
    -------
    poa : pd.DataFrame
        POA irradiance components, including ``poa_global``.
    """
    zenith = solar_position['apparent_zenith']
    azimuth = solar_position['azimuth']

    poa = pvlib.irradiance.get_total_irradiance(surface_tilt, surface_azimuth,
                                zenith, azimuth, dni, ghi, dhi, albedo=albedo,
                                airmass=airmass, dni_extra=dni_et, model='perez', **kwargs)

    # return the entire dataframe, not just poa_global, for component calculations
    return poa.fillna(0)

def half_interval_up(times):
    """
    shift a Datetimeindex forward by half an interval
    """
    shift_quantity=(times[1]-times[0])/2. #get what half a shift would be
    times+=shift_quantity
    return times

def half_interval_down(times):
    """
    shift a Datetimeindex forward by half an interval
    """
    shift_quantity=(times[1]-times[0])/2. #get what half a shift would be
    times-=shift_quantity
    return times
