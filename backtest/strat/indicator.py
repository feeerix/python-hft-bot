# Imports
import pandas as pd
import pandas_ta as ta
import inspect

# Local Imports
from lib.file.writer import *
from backtest.strat.settings import settings
from backtest.strat.composer import get_required_params, write_required_params


class indicator:
    def __init__(self, ind_func:ta, _settings:settings):
        # Add the func into the class
        self.ind_func = ind_func
        
        # Settings - a way to set up the indicator
        self.settings = _settings.settings
        # settings = {
        #     "name": setting_name
        #     "arguments": {  -> None df related arguments
        #         "arg1": default_value1,
        #         "arg2": default_value2
        #     }
        # }

    
    def print_settings(self):
        print(self.settings)

    def add_indicator(self, df:pd.DataFrame, verbose:bool=False) -> pd.DataFrame:
        
        # ta.stochrsi(close=df['close'], length=21, rsi_length=21, k=5, d=5)
        # df1 = ta.ema(df['close'], length=21)
        # df2 = ta.stochrsi(close=df['close'], length=21, rsi_length=21, k=5, d=5)

        # check if args include open high low close or volume
        ind_settings = {}
        req_params = get_required_params('ema')
        ohlcv = ['open', 'high', 'low', 'close', 'volume']
        for val in ohlcv:
            if val in req_params:
                ind_settings.update({val: df[val]})
        ind_settings.update(self.settings['arguments'])
        
        if verbose:
            print(ind_settings)
        return self.ind_func(**ind_settings)
    
