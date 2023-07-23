# Imports
import pandas as pd
import pandas_ta as ta

# Local Imports
from lib.file.writer import *
from backtest.strat.settings import settings
from backtest.strat.settings.settings import Settings
from backtest.strat.composer import get_required_params


class _Indicator:
    def __init__(self, _settings:Settings, verbose:bool=True, df:pd.DataFrame=None):
        # Verbosity
        self.verbose = verbose
        
        # Add the func into the class
        self.ind_func = getattr(ta, _settings.data['func_name'])
        
        # Settings - a way to set up the indicator
        self.settings = _settings

        # settings = {
        #     "name": setting_name,
        #     "func_name": func_name 
        #     "arguments": {
        #         "arg1": default_value1,
        #         "arg2": default_value2
        #     }
        # }

        if df is not None:
            self.df = self.ret_indicator(df)
    
    def print_settings(self):
        print(self.settings.data)

    def ret_indicator(self, df:pd.DataFrame) -> pd.DataFrame:
        # initialise empty settings
        ind_settings = {}

        # Get the required parameters (OHLCV)
        req_params = get_required_params(self.settings.data['func_name'])
        
        if self.verbose:
            print(f"PARAMS TO ADD: {self.settings.data['arguments']}")
        
        # OHLCV
        for argument in req_params.keys():
            
            if req_params[argument]:
                
                if argument.startswith('series_'):
                    ind_settings.update({argument: df[self.settings.data['arguments'][argument]]})
                
                elif (argument not in df.columns.to_list()) and type(self.settings.data['arguments'][argument]) != str:
                    ind_settings.update({argument: self.settings.data['arguments'][argument]})

                else: # OHLCV
                    ind_settings.update({argument: df[argument]})

            elif argument in self.settings.data['arguments'].keys():
                ind_settings.update({argument: self.settings.data['arguments'][argument]})
        
        ret_data = self.ind_func(**ind_settings)

        # Verbosity prints
        if self.verbose:
            print(ind_settings)
        
        # --------------------------------------------------------------
        if type(ret_data) == pd.DataFrame:
            self.settings.data['columns'] = ret_data.columns.tolist()
            return ret_data
        elif type(ret_data) == pd.Series:
            self.settings.data['columns'] = [ret_data.name]
            return pd.DataFrame(ret_data, columns=self.settings.data['columns'])
        else:
            print("SOMETHING WENT WRONG")
            print(type(ret_data))
            exit()
        
    


class Indicator:
    def __init__(self, _settings:settings, verbose:bool=True, df:pd.DataFrame=None):
        # Verbosity
        self.verbose = verbose
        
        # Add the func into the class
        self.ind_func = getattr(ta, _settings.data['func_name'])
        
        # Settings - a way to set up the indicator
        self.settings = _settings

        # settings = {
        #     "name": setting_name,
        #     "func_name": func_name 
        #     "arguments": {
        #         "arg1": default_value1,
        #         "arg2": default_value2
        #     }
        # }

        if df is not None:
            self.df = self.ret_indicator(df)
    
    def print_settings(self):
        print(self.settings.data)

    def ret_indicator(self, df:pd.DataFrame) -> pd.DataFrame:
        # initialise empty settings
        ind_settings = {}

        # Get the required parameters (OHLCV)
        req_params = get_required_params(self.settings.data['func_name'])
        
        if self.verbose:
            print(f"PARAMS TO ADD: {self.settings.data['arguments']}")
        
        # OHLCV
        for argument in req_params.keys():
            
            if req_params[argument]:
                
                if argument.startswith('series_'):
                    ind_settings.update({argument: df[self.settings.data['arguments'][argument]]})
                
                elif (argument not in df.columns.to_list()) and type(self.settings.data['arguments'][argument]) != str:
                    ind_settings.update({argument: self.settings.data['arguments'][argument]})

                else: # OHLCV
                    ind_settings.update({argument: df[argument]})

            elif argument in self.settings.data['arguments'].keys():
                ind_settings.update({argument: self.settings.data['arguments'][argument]})
        
        ret_data = self.ind_func(**ind_settings)

        # Verbosity prints
        if self.verbose:
            print(ind_settings)
        
        # --------------------------------------------------------------
        if type(ret_data) == pd.DataFrame:
            self.settings.data['columns'] = ret_data.columns.tolist()
            return ret_data
        elif type(ret_data) == pd.Series:
            self.settings.data['columns'] = [ret_data.name]
            return pd.DataFrame(ret_data, columns=self.settings.data['columns'])
        else:
            print("SOMETHING WENT WRONG")
            print(type(ret_data))
            exit()
        
    