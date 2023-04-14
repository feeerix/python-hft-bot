import pandas as pd
import pandas_ta as ta

from backtest.strat.indicator import indicator

class strategy:
    def __init__(self, name:str, verbose:bool=True): 
        self.name = name
        self.verbose = verbose
        self.df = None

    def init_df(self, df:pd.DataFrame):
        self.df = df

    def add_indicator(self, _indicator:indicator):
        # Add individual indicator
        self.df = pd.concat(
            [self.df, _indicator.ret_indicator(self.df, self.verbose)], 
            axis=1, 
            # ignore_index=True
        )
        # self.df = self.df[indicator.settings['columns']] = indicator.ind_func(indicator.settings.data['arguments'])

    # def add_condition(self, )    
    
    def add_entry(is_long:bool=False):
        # Long/short entries
        if is_long:
            pass

    def add_hardstop():
        # Make sure the bot doesn't get you liquidated and lose all your money
        pass

    