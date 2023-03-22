# Imports
import pandas as pd
import pandas_ta as ta


# Local Imports
from lib.api.binance.interface import Binance
from lib.api.binance.local import filename
from db.db import database
from strat.strat import strategy

class Backtester:
    def __init__(self):
        self.db = None

    def insert_strat(self, strategy:strategy):
        # Just make sure we have a db in place
        if self.db:
            self.db = self.db[strategy.settings['columns']] = strategy.indicator_type

    def test_strat(self):
        self.db = database().kline_df('ETHUSDT','1m',1640995200, 1672531200)

        # init db
        self.db = self.db[['stoch_rsi_k', 'stoch_rsi_d']] = ta.stochrsi(self.db['close'],window=14,smooth_k=3,smooth_d=3)
