"""Utilities for running Dashboard process"""

from __future__ import annotations

from collections import namedtuple
from datetime import (
    datetime,
    timedelta
)
import functools
import logging
from numbers import Number
import os
from pandas import (
    DataFrame,
    read_csv,
    read_excel
)
import re
import sys
from time import time
from typing import NewType

from ccrenew.dashboard.data_processing import Bluesky_weather_fucntions_v01 as blu
from ccrenew.dashboard import (
    all_df_keys,
    DateLike
)


# logger = logging.getLogger(__name__)

df_keys = all_df_keys

# NamedTuple for project parameters
ProjectParams = namedtuple('ProjectParams', ['project_name', 'ccr_id', 'tz', 'lat', 'lon', 'racking',
                                             'tilt_gcr', 'elevation', 'max_angle', 'temp_coef',
                                             'a_module', 'b_module', 'folder', 'axis_tilt', 'axis_azimuth', 'albedo'])

class FileNotFoundError(Exception):
    pass

class FileOpenError(Exception):
    pass

class project_dict(dict):
    def __repr__(self):
        print_str = ''
        for key, value in self.items():
            if value.processed:
                proc = ': Processed'
            else:
                proc = ': Unprocessed'
            print_str = print_str + key + proc + '\n'

        return print_str


def dict_insert(dict_, key, value):
    """Checks if a key already exists in dict, creates new key if not.
    Prevents overwriting of existing dictionary entries.

    Args:
        dict_ (dict): Dictionary to update.
        key (str): Key to check.
        value (str): Value to update if key doesn't exist.

    Returns:
        dict: Updated dictionary.
    """
    if key in dict_:
        pass
    else:
        dict_[key] = value
    return dict_

def picklefy_project_name(project_name):
    """Modifies the project name for pickling.

    Args:
        project_name (str): The "official" project name with spaces, commas, apostrophe's, and all that fun stuff
        year (int): The year to save for the pickle. Defaults to the current year.

    Returns:
        str: The picklefied project name.
    """
    project_name = re.sub(r"(,\s)|[,\s]", "_", project_name)
    project_name = re.sub(r"[']", "", project_name)

    return project_name

def get_snow_df(dashboard_folder, data_source, file_format):
    """Pulls snow data & returns a dataframe. Temporary fix for now, need to
    update path references

    Returns:
        DataFrame: Snow data
    """
    if file_format == 'xlsx':
        snow_file = os.path.join(dashboard_folder, 'Python_Functions', 'Snow Losses', '{}Operating-States-snowfall.xlsx'.format(data_source))
        raw_snow_df = read_excel(snow_file, index_col=0)
    else:
        snow_file = os.path.join(dashboard_folder, 'Python_Functions', 'Snow Losses', '{}Operating-States-snowfall.csv'.format(data_source))
        raw_snow_df = read_csv(snow_file, index_col=0)

    return raw_snow_df, snow_file

def retrieve_s3_df(bucket, key):
# helper function to get data from s3
    path = "s3://{b}/{k}".format(b=bucket, k=key)
    try:
        df = read_csv(path, index_col=0, parse_dates=True)
        df = df.loc[~df.index.duplicated(), :]
    except IOError:
        return DataFrame()
    return df

def run_bluesky(project_name: str, start: DateLike=None, end: DateLike=None, tran_ghi: str='add',
                convert: bool=False, resample: bool=True, ghi_index: int=0, axis_tilt: int=0,
                axis_azimuth: int=180, albedo: int=1, plot: bool=True, pool_size: int=6) -> DataFrame:
    """Pulls irradiance & weather data from Solcast for the project & date range.

    Args:
        project_name (str): The project to use for the Solcast script.
        start (str or datetime): The start date for Solcast data. Default
            will set it to the first day of the current month.
        end (str or datetime): The end date for Solcast data. Default will
            set it to the day before the current date. Known by some as yesterday.
        tran_ghi (str): Option to run the script to transpose GHI for POA.
            
            * Options:
                * `add` to add it to the df_cats dataframe.
                * `only` to pull just the transposed GHI & not df_cats.
                * `none` to pull just df_cats.

        convert (bool): Option to convert units.    
        resample (bool): Option to convert from DAS frequency to hourly.
        ghi_index (int): 0-based index of GHI to use when running the transposed GHI script.
        axis_tilt (int): 
        plot (bool): Option to draw plots of the data from solcast.

    Returns:
        df_solcast (pd.DataFrame): The Solcast irradiance & weather data.
    """
    

    # Grab project parameters
    params = _get_project_params(project_name=project_name, axis_tilt=axis_tilt,
                                 axis_azimuth=axis_azimuth, albedo=albedo)

    # Get default dates if not provided.
    if not start:
        today = datetime.today()
        # If it's the first of the month we'll just subtract 30 days to make it easy
        if today.day == 1:
            start = today - timedelta(days=30)
        else:
            start = datetime(today.year, today.month, 1)
    if not end:
        today = datetime.today()
        end = today - timedelta(days=1)

    # Initialized dfs
    df_solcast = DataFrame()
    df_tran_ghi = DataFrame()

    # Pull satellite data if `tran_ghi` is 'add' or 'none'
    if tran_ghi != 'only':
        source = 'satellite'
        df_weather = blu.get_weather_data(start=start, end=end, params=params, source=source,
                                          convert=convert, pool_size=pool_size)
        df_solcast = blu.calculate_poa(df_weather=df_weather, source=source, params=params, resample=resample)
        df_solcast = df_solcast.reindex(columns=['poa', 'Tamb', 'Tmod', 'Wind_speed', 'ghi'])

    # Pull measured data if `tran_ghi` is 'add' or 'only'
    if tran_ghi != 'none':
        source = 'measured'
        df_weather = blu.get_weather_data(start=start, end=end, params=params, source=source,
                                          convert=convert, pool_size=pool_size)

        # Grab the ghi column if exists
        try:
            ghi_col = [col for col in df_weather.columns if 'GHI' in col][ghi_index]
            df_weather = df_weather[[ghi_col]].rename(columns={ghi_col: 'ghi'})
            df_poa = blu.calculate_poa(df_weather=df_weather, source=source, params=params, resample=resample)
            df_tran_ghi = df_poa[['poa']].rename(columns={'poa': 'sites_ghi_poa'})
        except IndexError:
            print('No GHI to transpose! Solcast POA only')

    # If either df is empty we'll either use the satellite or transposed data
    if any([df_solcast.empty, df_tran_ghi.empty]):
        if df_solcast.empty:
            df_solcast = df_tran_ghi
    # If neither df is empty we'll add the transposed GHI to the satellite data
    else:
        df_solcast.loc[:, 'sites_ghi_poa'] = df_tran_ghi

    if plot:
        df_solcast.reindex(columns=['ghi', 'poa', 'sites_ghi_poa']).plot()

    # Add project name to df so we can tell which site we're looking at
    df_solcast.index.name = project_name

    print('\n')
    print('Solcast data successfully returned for {}'.format(project_name))
    print('\n')
    return df_solcast

def _get_project_params(project_name: str, axis_tilt: int, axis_azimuth: int, albedo: int):
    df_proj_keys = df_keys.query("Project == @project_name").to_dict('records')[0]
    project_params = ProjectParams(
        project_name,
        df_proj_keys['CCR_ID'],
        f"US/{df_proj_keys['Timezone']}",
        df_proj_keys['GPS_Lat'],
        df_proj_keys['GPS_Long'],
        df_proj_keys['Racking'],
        df_proj_keys['Tilt/GCR'],
        df_proj_keys['Elevation'],
        df_proj_keys['Max_angle'],
        df_proj_keys['Temp_Coeff_Pmax'],
        df_proj_keys['a_module'],
        df_proj_keys['b_module'],
        df_proj_keys['Folder'],
        axis_tilt,
        axis_azimuth,
        albedo
    )

    return project_params

# Decorator function for timing the execution of functions
def func_timer(func):
    """Decorator for timing the execution of functions.

    Args:
        func (function): Function to time.
    """
    # Initiate logger
    logger = logging.getLogger('timer')

    @functools.wraps(func)
    def timer(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        elapsed = time() - start

        # Build custom message for the logger so it doesn't just show that each
        # call came from the `timer()` function
        # Python 2 compatibility
        # Python 2 compatibility
        if sys.version_info.major == 3:
            file_str = 'File: {}'.format(os.path.basename(func.__code__.co_filename))
            line_str = 'Line: {}'.format(func.__code__.co_firstlineno)
        else:
            file_str = 'File: {}'.format(os.path.basename(func.func_code.co_filename))
            line_str = 'Line: {}'.format(func.func_code.co_firstlineno)

        log_msg = {
            'file': file_str,
            'module': 'Module: {}'.format(func.__module__),
            'function': 'Function: {}'.format(func.__name__),
            'line_no': line_str,
            'func_name': func.__name__,
            'elapsed': elapsed
        }
        # Check if the function call comes from a project, if so we'll add the project name to the log message
        try:
            log_msg['project_name'] = args[0].project_name
            message = '{file}\t{module}\t{function}\t{line_no}\tFunction call `{func_name}` for {project_name} complete. Total time: {elapsed:7.3f}s'.format(**log_msg)
        except AttributeError:
            message = '{file}\t{module}\t{function}\t{line_no}\tFunction call `{func_name}` complete. Total time: {elapsed:7.3f}s'.format(**log_msg)
        logger.debug(message)

        return result
    return timer

def update_config(func):
    """Decorator to update the config file if necessary before running a function.

    Args:
        func (function): Function that will need an updated config file.
    """
    @functools.wraps(func)
    def check_config(self, *args, **kwargs):
        if self.last_update_config != os.path.getmtime(self.config_filepath):
            self._parse_config_file()
        return func(self, *args, **kwargs)
    return check_config
