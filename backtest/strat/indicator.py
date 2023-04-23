# Imports
import pandas as pd
import pandas_ta as ta
import inspect

# Local Imports
from lib.file.writer import *
from backtest.strat.settings import settings
from backtest.strat.composer import get_required_params, write_required_params


class indicator:
    def __init__(self, _settings:settings):
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
    
    def print_settings(self):
        print(self.settings.data)

    def ret_indicator(self, df:pd.DataFrame, verbose:bool=False) -> pd.DataFrame:
        # initialise empty settings
        ind_settings = {}

        # Get the required parameters (OHLCV)
        req_params = get_required_params(self.settings.data['func_name'])
        
        if self.settings.utility:
            ind_settings.update({'series_a': df[self.settings.data['arguments']['series_a']]})
            ind_settings.update({'series_b': df[self.settings.data['arguments']['series_b']]})
            # TODO - Putting in for cross function for now - to update to be dynamic
            if 'above' in self.settings.data['arguments'].keys():
                ind_settings.update({'above': self.settings.data['arguments']['above']})

        else:
            # initialise ohlcv
            ohlcv = ['open', 'high', 'low', 'close', 'volume']

            # For for the list
            for val in ohlcv:
                # check if args include open high low close or volume
                if val in req_params:
                    ind_settings.update({val: df[val]})

        # Verbosity prints
        if verbose:
            print(ind_settings)
            exit()
        
        # Return
        if self.settings.utility:
            ret_data = self.ind_func(**ind_settings)
        else:
            # Add settings to indicator settings
            ind_settings.update(self.settings.data['arguments'])

            # call ta function
            ret_data = self.ind_func(**ind_settings)

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
        
        
    
