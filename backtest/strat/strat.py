import pandas as pd
import pandas_ta as ta

from backtest.strat.indicator import indicator

class strategy:
    def __init__(self, name:str): 
        self.name = name

    def add_indicator(self, df:pd.DataFrame, indicator:indicator):
        # Add individual indicator
        # df = df[indicator.settings['columns']] = indicator.indicator_type(indicator.settings[''])
        pass


    def add_entry():
        # Long/short entries
        pass

    def add_hardstop():
        # Make sure the bot doesn't get you liquidated
        pass

