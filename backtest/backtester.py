# Imports
import pandas as pd
import pandas_ta as ta


# Local Imports
from lib.api.binance.interface import Binance
from lib.api.binance.local import filename
from db.db import database
from backtest.strat.indicator import indicator
from backtest.strat.settings import settings
from backtest.strat.strat import strategy
test = settings("stochrsi", "stochrsi", {'length':21,'rsi_length':21,'k':5,'d':5}, verbose=False)

# For testing
test_settings_list = [
    settings("stochrsi", "stochrsi", {'length':21,'rsi_length':21,'k':5,'d':5}, verbose=False),
    settings("ema8", "ema", {'length': 8}, verbose=False),
    settings("ema21", "ema", {'length': 21}, verbose=False),
    settings("ema144", "ema", {'length': 144}, verbose=False),
    settings("ema233", "ema", {'length': 233}, verbose=False),
    settings("8above21", "above", {'series_a':'EMA_8','series_b':'EMA_21'}),
    settings("8below21", "below", {'series_a':'EMA_8','series_b':'EMA_21'}),
    settings("144above233", "above", {'series_a':'EMA_144','series_b':'EMA_233'}),
    settings("144below233", "below", {'series_a':'EMA_144','series_b':'EMA_233'}),
    settings("stochrsi", "above", {'series_a':'STOCHRSIk_21_21_5_5','series_b':'STOCHRSId_21_21_5_5'}),
    settings("stochrsi", "below", {'series_a':'STOCHRSIk_21_21_5_5','series_b':'STOCHRSId_21_21_5_5'}),
]

long1 = settings("long1","long",{"open":{1:["EMA_8_B_EMA_21", "EMA_144_A_EMA_233"],0:[]}, "close":{1:[],0:[]}})
short1 = settings("short1","short",{"open":{1:["EMA_8_A_EMA_21", "EMA_144_B_EMA_233"],0:[]}, "close":{1:[],0:[]}})


class Backtester:
    def __init__(self):
        
        self.db = None
        self.strategy = None

    def create_db(self, symbol:str, interval:str, starttime:int, endtime:int):
        self.db = database().kline_df(symbol, interval, starttime, endtime)

    def insert_strat(self, name:str, _strategy:strategy):
        # Just make sure we have a db in place
        # def __init__(self, name:str, verbose:bool=True): 
        
        self.strategy = _strategy(name)
        self.strategy.init(self.db)
        # TODO - to add the correct insertion here
        # print("something went wrong!")
        # exit()

    def test_strat(self):
        start = 1640995200
        end = 1672531200
        self.create_db('ETHUSDT', '1m', start, end)
        self.insert_strat(strategy("test_name"))

        for _indicator in test_settings_list:
            self.strategy.add_indicator(_indicator)

        self.add_entry(long1)
        self.add_entry(short1)


    def start_test(self, initial_capital:int):
        pass