# Imports
import pandas as pd
import pandas_ta as ta

# Local Imports
from lib.file.writer import *
# from backtest.strat.settings import settings
from backtest.strat.settings.settings import Settings
from backtest.strat.composer import get_required_params
from lib.tools.interval import Interval


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
        I just need to start shipping this thing, fuck.
        """
        self.interval = _interval

        """
        Build the dataframe when provided and place it in the signal class.
        This will mean if you input the dataframe straight awaiy it will start building.
        Not sure if we want this behaviour yet or not.
        """

        if df is not None:
            self.df = self.build_signal(df)

    
    def __str__(self) -> str:
        return f"SIGNAL -- {self.settings.name}-{self.settings.columns}"

    @property
    def columns(self):
        return self.settings.columns
    
    def build_signal(self, df:pd.DataFrame) -> pd.DataFrame:
        # initialise empty settings
        ind_settings = {}

        # Get the required parameters (OHLCV)
        req_params = get_required_params(self.settings.func_name)
        
        # OHLCV
        for argument in req_params.keys():
            
            if req_params[argument]:
                
                if argument.startswith('series_'):
                    print(df.columns.tolist())
                    print(argument)
                    exit()
                    ind_settings.update({argument: df[self.settings.arguments[argument]]})
                
                elif (argument not in df.columns.to_list()) and type(self.settings.arguments[argument]) != str:
                    ind_settings.update({argument: self.settings.arguments[argument]})

                else: # OHLCV
                    ind_settings.update({argument: df[argument]})

            elif argument in self.settings.data.arguments.keys():
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
        
    