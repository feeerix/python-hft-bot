# Imports
import pandas as pd
import pandas_ta as ta
import inspect

# Local Imports
from lib.file.writer import *
from backtest.strat.settings import settings



class indicator:
    def __init__(self, ind_func:ta, _settings:settings):
        # Add the func into the class
        self.ind_func = ind_func
        
        # Settings - a way to set up the indicator
        self.settings = _settings.settings
        # settings = {
        #     "name": setting_name
        #     "arguments": {
        #         "arg1": default_value1,
        #         "arg2": default_value2
        #     }
        # }

    
    def print_settings(self):
        print(self.settings)

    def add_indicator(self, df:pd.DataFrame) -> pd.DataFrame:
        # ta.stochrsi(close=df['close'], length=21, rsi_length=21, k=5, d=5)
        df['ema'] = self.ind_func(self.settings['arguments'])
        return df
        
    
