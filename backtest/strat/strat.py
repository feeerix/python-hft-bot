# Imports
import pandas as pd
import pandas_ta as ta
import numpy as np

# Local Imports
from backtest.strat.indicator import indicator
from backtest.strat.settings import settings

class strategy:
    def __init__(self, name:str, verbose:bool=True): 
        self.name = name
        self.verbose = verbose
        self.df = None
        # ------------------
        # indicator_example = [
        #     {
        #         indicator.settings.data
        #     }, ...
        # ]
        self.indicator_settings_list = []
        # ------------------

        self.longshort_condition_settings = {
            "long": [],
            "short": []
        }

    def init_df(self, df:pd.DataFrame):
        self.df = df
        self.df['in_position'] = 0

    def add_indicator(self, _indicator:indicator):
        self.indicator_list.append(_indicator)

        # Add individual indicator
        self.df = pd.concat(
            [self.df, _indicator.ret_indicator(self.df, self.verbose)], 
            axis=1, 
            # ignore_index=True
        )

    
    def add_entry(self, _settings:settings):
        # Long/short entries

        if self.verbose:
            print(_settings.data)

        self.df[_settings.data['name']] = np.where((
                (self.df[_settings.data['arguments']['open'][1]].all(axis=1)) &
                (self.df[_settings.data['arguments']['open'][0]].sum(axis=1) == 0)
            ), 1, 0)
        


    def add_close(self, position_id: int):
        pass

    def add_hardstop():
        # Make sure the bot doesn't get you liquidated and lose all your money
        pass

    