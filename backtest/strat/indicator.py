# Imports
import pandas as pd
import pandas_ta as ta

# Local Imports
from lib.file.writer import *
# from backtest.strat.settings import settings
from backtest.strat.settings.settings import Settings
from backtest.strat.composer import get_required_params

# ema8 = Indicator(Settings("ema8", "ema", {'length': 8}))
# ema21 = Indicator(Settings("ema21", "ema", {'length': 21}))
# ema144 = Indicator(Settings("ema144", "ema", {'length': 144}))
# ema233 = Indicator(Settings("ema233", "ema", {'length': 233}))
# stochrsi = Indicator(Settings("stochrsi", "stochrsi", {"length": 21, "rsi_length": 21, "k": 5, "d": 5}))

class Indicator:
    def __init__(self, _settings:Settings, verbose:bool=True, df:pd.DataFrame=None):
        # Verbosity
        self.verbose = verbose
        
        # Add the func into the class
        self.ind_func = getattr(ta, _settings.func_name)
        
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
        req_params = get_required_params(self.settings.func_name)
        
        # OHLCV
        for argument in req_params.keys():
            
            if req_params[argument]:
                
                if argument.startswith('series_'):
                    ind_settings.update({argument: df[self.settings.arguments[argument]]})
                
                elif (argument not in df.columns.to_list()) and type(self.settings.data['arguments'][argument]) != str:
                    ind_settings.update({argument: self.settings.arguments[argument]})

                else: # OHLCV
                    ind_settings.update({argument: df[argument]})

            elif argument in self.settings.arguments.keys():
                ind_settings.update({argument: self.settings.arguments[argument]})
        
        ret_data = self.ind_func(**ind_settings)

        
        # --------------------------------------------------------------
        if type(ret_data) == pd.DataFrame:
            self.settings.columns = ret_data.columns.tolist()
            return ret_data
        elif type(ret_data) == pd.Series:
            self.settings.columns = [ret_data.name]
            return pd.DataFrame(ret_data, columns=self.settings.columns)
        else:
            print("SOMETHING WENT WRONG")
            print(type(ret_data))
            exit() # PANIC
        
    