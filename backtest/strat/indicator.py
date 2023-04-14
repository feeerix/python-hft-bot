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
        #     "name": setting_name
        #     "columns": []
        #     "arguments": {  -> None df related arguments
        #         "arg1": default_value1,
        #         "arg2": default_value2
        #     }
        # }
    
    def print_settings(self):
        print(self.settings.data)

    def ret_indicator(self, df:pd.DataFrame, verbose:bool=False) -> pd.DataFrame:

        # initialise empty settings
        ind_settings = {}
        # initialise ohlcv
        ohlcv = ['open', 'high', 'low', 'close', 'volume']

        # Get the required parameters (OHLCV)
        req_params = get_required_params('ema')

        # For for the list
        for val in ohlcv:
            # check if args include open high low close or volume
            if val in req_params:
                ind_settings.update({val: df[val]})
        
        # Add settings to indicator settings
        ind_settings.update(self.settings.data['arguments'])
        
        # Verbosity prints
        if verbose:
            print(ind_settings)

        # Return
        ret_data = self.ind_func(**ind_settings)
        if type(ret_data) == pd.DataFrame:
            self.settings.data['columns'] = ret_data.columns.tolist()
            return ret_data
        else:
            self.settings.data['columns'] = [ret_data.name]
            return pd.DataFrame(ret_data, columns=self.settings.data['columns'])

        
        
    
