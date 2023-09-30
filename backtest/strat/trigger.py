# Imports
import pandas as pd
import pandas_ta as ta
from typing import List

# Local Imports
from lib.file.writer import *
# from backtest.strat.settings import settings
from backtest.strat.settings.settings import Settings
from backtest.strat.composer import get_required_params
from lib.tools.interval import Interval


class Trigger:
    def __init__(self, _settings:Settings, _interval:Interval, verbose:bool=True, df:pd.DataFrame=None):
        # Verbosity
        self.verbose = verbose
        
        # Add the func into the class
        self.ind_func = getattr(ta, _settings.func_name)
        
        # Settings - a way to set up the indicator
        self.settings = _settings
        self.interval = _interval

        if df is not None:
            self.df = self.build_trigger(df)

    
    def __str__(self) -> str:
        return f"TRIGGER -- {self.settings.name}-{self.settings.columns}"
    

    def check(self, row:tuple, lookback:int=0) -> bool:
        """
        This is the function that's used to check if a trigger is valid
        or not.
        """

        self.settings.func_name

        # _utility = ('above', 'above_value', 'below', 'below_value', 'cross')
        pass
    

class Trigger:
    def __init__(self, _settings:Settings, _interval:Interval, verbose:bool=True, df:pd.DataFrame=None):
        # Verbosity
        self.verbose = verbose
        
        # Add the func into the class
        self.ind_func = getattr(ta, _settings.func_name)
        
        # Settings - a way to set up the indicator
        self.settings = _settings

        self.interval = _interval

        if df is not None:
            self.df = self.build_trigger(df)

    
    def __str__(self) -> str:
        return f"SIGNAL -- {self.settings.name}-{self.settings.columns}"

    @property
    def columns(self):
        return self.settings.columns
    
    def check(self, row:List[tuple], column_a:str, column_b: str, lookback:int=0):
        """
        This function will take in a list of rows, minimum of length 1, which is 
        always the length of the lookback.

        The bottom row in the list is the latest OHLCV row.

        This will perform the check based on the setting presented.
        """
        # _utility = ('above', 'above_value', 'below', 'below_value', 'cross')
        pass
    
    def build_trigger(self, df:pd.DataFrame) -> pd.DataFrame:
        # initialise empty settings
        ind_settings = {}

        # Get the required parameters (OHLCV)
        req_params = get_required_params(self.settings.func_name)
        if self.verbose:
            print(f"ADDING: {self.settings.func_name}")

        # OHLCV

        for argument in req_params.keys():
            
            if req_params[argument]:
                
                if argument.startswith('series_'):
                    ind_settings.update({argument: df[self.settings.arguments[argument]]})
                
                elif (argument not in df.columns.to_list()) and type(self.settings.arguments[argument]) != str:
                    ind_settings.update({argument: self.settings.arguments[argument]})

                else: # OHLCV
                    ind_settings.update({argument: df[argument]})

            elif argument in self.settings.arguments.keys():
                ind_settings.update({argument: self.settings.arguments[argument]})
        
        
        ret_data = self.ind_func(**ind_settings)

        # --------------------------------------------------------------
        if type(ret_data) == pd.DataFrame:
            return pd.concat(df, ret_data, axis=1)
            
        elif type(ret_data) == pd.Series:
            self.settings.columns = [ret_data.name]
            return pd.concat([df, pd.DataFrame(ret_data, columns=self.settings.columns)], axis=1)

        else:
            print("SOMETHING WENT WRONG")
            print(type(ret_data))
            exit() # PANIC
        
    