# Imports
import pandas as pd
import pandas_ta as ta

# Local Imports
from lib.file.writer import *
# from backtest.strat.settings import settings
from backtest.strat.settings.settings import Settings
from backtest.strat.composer import get_required_params


# signal_indicators = [
#     Indicator(Settings("144Above233_bullish", "above", {"series_a": "EMA_144", "series_b": "EMA_233"})),
#     Indicator(Settings("144Below233_bearish", "below", {"series_a": "EMA_144", "series_b": "EMA_233"})),
#     Indicator(Settings("ema8below_ema21", "below", {"series_a": "EMA_8", "series_b": "EMA_21"})),
#     Indicator(Settings("ema8above_ema21", "above", {"series_a": "EMA_8", "series_b": "EMA_21"})),
#     Indicator(Settings("stochrsi_oversold_k", "below_value", {"series_a": "STOCHRSIk_34_34_8_8", "value": 20.0})),
#     Indicator(Settings("stochrsi_oversold_d", "below_value", {"series_a": "STOCHRSId_34_34_8_8", "value": 20.0})),
#     Indicator(Settings("stochrsi_overbought_k", "above_value", {"series_a": "STOCHRSIk_34_34_8_8", "value": 80.0})),
#     Indicator(Settings("stochrsi_overbought_d", "above_value", {"series_a": "STOCHRSId_34_34_8_8", "value": 80.0})),
#     Indicator(Settings("stochrsi_bullcross", "cross", {"series_a": "STOCHRSIk_34_34_8_8", "series_b": "STOCHRSId_34_34_8_8"})),
#     Indicator(Settings("stochrsi_bullcross", "cross", {"series_a": "STOCHRSIk_34_34_8_8", "series_b": "STOCHRSId_34_34_8_8", "above": False}))
# ]

class Signal:
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
    
    def __str__(self) -> str:
        return f"{self.settings.data['name']}-{self.settings.data['columns']}"

    @property
    def columns(self):
        return self.settings.data['columns']

    def ret_indicator(self, df:pd.DataFrame) -> pd.DataFrame:
        # initialise empty settings
        ind_settings = {}

        # Get the required parameters (OHLCV)
        req_params = get_required_params(self.settings.data['func_name'])
        
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
            exit() # PANIC
        
    