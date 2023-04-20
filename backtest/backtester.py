# Imports
import pandas as pd
import pandas_ta as ta


# Local Imports
from lib.api.binance.interface import Binance
from lib.api.binance.local import filename
from db.db import database
from backtest.strat.indicator import indicator
# from backtest.strat.settings import settings
from backtest.strat.settings.settings import settings
from backtest.strat.strat import strategy


# test1 = settings("stochrsi", "stochrsi", {'length':21,'rsi_length':21,'k':5,'d':5}, verbose=False)
# test2 = settings("ema8", "ema", {'length': 8}, verbose=False)
# exit()
# settings("ema21", "ema", {'length': 21}, verbose=False)
# settings("ema144", "ema", {'length': 144}, verbose=False)
# settings("ema233", "ema", {'length': 233}, verbose=False)
# settings("8above21", "above", {'series_a':'EMA_8','series_b':'EMA_21'})
# settings("8below21", "below", {'series_a':'EMA_8','series_b':'EMA_21'})
# settings("144above233", "above", {'series_a':'EMA_144','series_b':'EMA_233'})
# settings("144below233", "below", {'series_a':'EMA_144','series_b':'EMA_233'})
# settings("stochrsi", "above", {'series_a':'STOCHRSIk_21_21_5_5','series_b':'STOCHRSId_21_21_5_5'})
# settings("stochrsi", "below", {'series_a':'STOCHRSIk_21_21_5_5','series_b':'STOCHRSId_21_21_5_5'})


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

    def test_strat(self):
        start = 1640995200
        end = 1672531200
        self.create_db('ETHUSDT', '1m', start, end)
        test_strat = strategy("test_strat", self.db, False)
        # test_strat.init_df(self.db)

        for _indicator_settings in test_settings_list:
            test_strat.add_indicator(indicator(_indicator_settings))

        test_strat.add_entry(long1)
        test_strat.add_entry(short1)
        

        print(test_strat.df)

        position = None
        opening_price = None
        closing_price = None
        positions = []
        # Loop through rows
        for i, row in test_strat.df.iterrows():
            # If long position is possible and no position is open, open long position
            if row['long1'] == 1 and position is None:
                position = 'long'
                opening_price = row['Close']
            # If short position is possible and no position is open, open short position
            elif row['short1'] == 1 and position is None:
                position = 'short'
                opening_price = row['Close']
            # If long position is open and long_close is 1, close long position and calculate profit
            elif position == 'long' and row['long_close'] == 1:
                closing_price = row['Close']
                profit = closing_price - opening_price
                positions.append({
                    'Open Time': test_strat.df.iloc[i-1].name,
                    'Close Time': row.name,
                    'Type': 'long',
                    'Opening Price': opening_price,
                    'Closing Price': closing_price,
                    'Profit': profit
                })
                position = None
                opening_price = None
                closing_price = None
            # If short position is open and short_close is 1, close short position and calculate profit
            elif position == 'short' and row['short_close'] == 1:
                closing_price = row['Close']
                profit = opening_price - closing_price
                positions.append({
                    'Open Time': test_strat.df.iloc[i-1].name,
                    'Close Time': row.name,
            'Type': 'short',
            'Opening Price': opening_price,
            'Closing Price': closing_price,
            'Profit': profit
        })
        position = None
        opening_price = None
        closing_price = None

        # Create positions dataframe
        positions_df = pd.DataFrame(positions)
        print(positions_df)


    def start_test(self, initial_capital:int):
        pass