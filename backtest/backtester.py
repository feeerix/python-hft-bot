# Imports
import pandas as pd
import pandas_ta as ta


# Local Imports
from lib.api.binance.interface import Binance
from lib.api.binance.local import filename
from db.db import database


class Backtester:
    def __init__(self):
        pass

    def insert_strat(self, strategy:dict):
        pass

    def test_strat(self):
        kline_db = database().kline_df('ETHUSDT','1m',1640995200, 1672531200)

        # init db
        kline_db[['stoch_rsi_k', 'stoch_rsi_d']] = ta.stochrsi(kline_db['close'],window=14,smooth_k=3,smooth_d=3)

        print(kline_db)