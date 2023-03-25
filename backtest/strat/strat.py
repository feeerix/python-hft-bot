import pandas as pd
import pandas_ta as ta

from backtest.strat.indicator import indicator

class strategy:
    def __init__(self, name:str): 
        self.name = name
        self.df = None

    def init_df(self, df:pd.DataFrame):
        self.df = df

    def add_indicator(self, indicator:indicator):
        # Add individual indicator
        self.df = self.df[indicator.settings['columns']] = indicator.ind_func(indicator.settings['arguments'])
        
    def add_entry():
        # Long/short entries
        pass

    def add_hardstop():
        # Make sure the bot doesn't get you liquidated and lose all your money
        pass

    