# Imports
import pandas as pd
import pandas_ta as ta

# Local Imports
from lib.file.writer import *
from backtest.strat.settings.settings import Settings
from backtest.strat.composer import get_required_params
from lib.tools.interval import Interval


class Logic:
    def __init__(self, _settings:Settings, _interval:Interval, verbose:bool=True, df:pd.DataFrame=None):
        # Verbosity
        self.verbose = verbose
        
        # Add the func into the class
        self.ind_func = getattr(ta, _settings.func_name)
        
        # Settings - a way to set up the indicator
        self.settings = _settings

        """
        Relates to the interval we want to reference.
        If there is a signal that requires multiple intervals we will do this in logic
        as we look at this from a database perspective?
        """
        self.interval = _interval

        if df is not None:
            self.df = self.build_signal(df)

    
    def __str__(self) -> str:
        return f"SIGNAL -- {self.settings.name}-{self.settings.columns}"

    @property
    def columns(self):
        return self.settings.columns
    
    @property
    def plumbing(self):
        """
        Defines how the logic works and will be derived based on the settings.
        It can then be checked if logic is true, and then be executed.
        """
        pass

    def execute(self):
        pass

    def check(self) -> bool:
        """
        This is returns a boolean if the specific logic has been met.
        """
        
    


    def build_signal(self, df:pd.DataFrame) -> pd.DataFrame:
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
        
    