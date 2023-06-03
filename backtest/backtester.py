# Imports
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timezone
import hashlib

# Local Imports
from lib.api.binance.interface import Binance
from lib.api.binance.local import filename
from lib.file.writer import *
from lib.file.reader import *

from db.db import database

from backtest.strat.indicator import indicator
from backtest.strat.settings.settings import settings
from backtest.strat.strat import strategy

from lib.cli.printer import line

class Backtester:
    def __init__(self, verbose:bool=False):
        
        self.db = None
        self.strategy = None
        self.verbose = verbose

    def create_db(self, symbol:str, interval:str, starttime:int, endtime:int):
        self.db = database().kline_df(symbol, interval, starttime, endtime)

    def compute_results(self, positions_df:pd.DataFrame, df:pd.DataFrame, init_capital: int):
        # TODO - eventually return this in a json and can write everything to file and give it a datetime + name
        print(line)
        print("RESULTS DATA")
        print(positions_df)

        wins = (positions_df['Profit'] > 0).sum()
        losses = (positions_df['Profit'] < 0).sum()
        start = datetime.fromtimestamp(df['time'].iloc[0]/1000, tz=timezone.utc)
        end = datetime.fromtimestamp(df['time'].iloc[-1]/1000, tz=timezone.utc)

        print(f"START TIME: {start.strftime('%DD/%MM/%YYYY %H:%M:%S')}")
        print(f"END TIME: {end.strftime('%DD/%MM/%YYYY %H:%M:%S')}")

        print(f"DURATION: {divmod((end-start).total_seconds(), 86400)[0]} DAYS")

        print(f"NET PROFIT: {positions_df['Profit'].sum(axis=0)}")
        print(f"PCT RETURN: {round(((positions_df['Capital'].iloc[-1] - init_capital)/init_capital)*100, 3)}")
        
        print(f"GROSS PROFIT: {positions_df.loc[positions_df['Profit'] > 0, 'Profit'].sum()}")
        print(f"GROSS LOSS: {positions_df.loc[positions_df['Profit'] < 0, 'Profit'].sum()}")
        
        print(f'WINS: {wins}')
        print(f'LOSSES: {losses}')
        print(f"WIN RATE: {round((wins / (losses + wins)) * 100, 3)}%")

        avg_win = positions_df.loc[positions_df['Profit'] > 0, 'Profit'].mean()
        avg_loss = positions_df.loc[positions_df['Profit'] < 0, 'Profit'].mean()

        print(f"MEAN WIN: {round(avg_win, 3)}")
        print(f"MEDIAN WIN: {round(positions_df.loc[positions_df['Profit'] > 0, 'Profit'].median(), 3)}")
        
        print(f"MEAN LOSS: {round(avg_loss, 3)}")
        print(f"MEDIAN LOSS: {round(positions_df.loc[positions_df['Profit'] < 0, 'Profit'].median(), 3)}")

        # positions_df['Duration'] = positions_df['Close Time'] - positions_df['Open Time']
        # avg_duration_win = positions_df.loc[positions_df['Profit'] > 0, 'Duration'].mean()
        # avg_duration_loss = positions_df.loc[positions_df['Profit'] < 0, 'Duration'].mean()
        # avg_duration_win_mins = avg_duration_win / 60
        # avg_duration_loss_mins = avg_duration_loss / 60

        # print(f"AVERAGE HOLDING TIME FOR WINS: {avg_duration_win_mins} minutes")
        # print(f"AVERAGE HOLDING TIME FOR LOSSES: {avg_duration_loss_mins} minutes")

        # print(f"AVERAGER HOLDING TIME: {round(((positions_df['Close Time'] - positions_df['Open Time']).mean() / 60), 3)} minutes")

        print(f"AVG R/R: {round(avg_win/abs(avg_loss),3)}")

        print(f"MAX WIN: {positions_df.loc[positions_df['Profit'] > 0, 'Profit'].max()}")
        print(f"MAX LOSS: {positions_df.loc[positions_df['Profit'] < 0, 'Profit'].min()}")
        
        print(f"MAX DRAWDOWN PERCENT: {ta.drawdown(positions_df['Capital'])['DD_PCT'].max()}")

        print(f"BUY AND HOLD RETURN: {(df['close'].iloc[-1] - df['open'].iloc[0]) / df['open'].iloc[0]}")

        print(f"SHARPE RATIO: {ta.sharpe_ratio(positions_df['Capital'], period=365)}")
        # print(f"SORTINO RATIO: {ta.sortino_ratio(positions_df['Capital'])}")
        positions_df['Returns PCT'] = positions_df['Capital'].pct_change()
        print(f"AVERAGE RETURN: {positions_df['Returns PCT'].mean()}")
        print(f"RETURNS STD DEV: {positions_df['Returns PCT'].std()}")
        print(line)

    def test_run(self, test_strat:strategy, capital:float):
        ohlc = ['open', 'high', 'low', 'close']
        # To update
        init_capital = capital

        
        position = None
        opening_price = None
        closing_price = None
        positions = []
        position_size = 0

        # To define resolution for bar
        distance = len(test_strat.df.index)
        if distance > 500000:
            resolution = 10000
        elif distance > 100000:
            resolution = 1000
        else:
            resolution = 100

        # Loop through rows
        for i, row in test_strat.df.iterrows():

            if capital < 0:
                print("You went broke!")
                break

            if self.verbose:
                if (i % resolution) == 0:
                    print(f"{round((i/distance)*100, 3)}% COMPLETE")

            
            # If long position is possible and no position is open, open long position
            if row['long1'] == 1 and position is None:
                position = 'long'
                opening_price = row['close']

                position_size = capital / opening_price
                take_profit = opening_price + (test_strat.df.loc[i, 'ATRe_21'] * 4)
                stop_loss = opening_price - (test_strat.df.loc[i, 'ATRe_21'] * 0.25)

            # If short position is possible and no position is open, open short position
            elif row['short1'] == 1 and position is None:
                position = 'short'
                opening_price = row['close']

                position_size = capital / opening_price
                take_profit = opening_price - (test_strat.df.loc[i, 'ATRe_21'] * 4)
                stop_loss = opening_price + (test_strat.df.loc[i, 'ATRe_21'] * 0.25)
            
            # If long position is open and long_close is 1, close long position and calculate profit
            elif position == 'long':
                if any(test_strat.df.loc[i, price] > opening_price for price in ['close']):
                    stop_loss = opening_price

                if row['long1_close'] == 1:
                    if any(test_strat.df.loc[i, price] < stop_loss for price in ohlc):
                        closing_price = stop_loss

                    elif  any(test_strat.df.loc[i, price] > take_profit for price in ohlc):
                        closing_price = take_profit

                    else:
                        closing_price = row['close']

                    profit = position_size * (closing_price - opening_price)
                    capital += profit
                    
                    positions.append({
                        'Open Time': test_strat.df['time'].iloc[i-1],
                        'Close Time': row['time'],
                        'Type': 'long',
                        'Opening Price': opening_price,
                        'Closing Price': closing_price,
                        'Take Profit': take_profit,
                        'Stop Loss': stop_loss,
                        'Profit': profit,
                        'Capital': capital
                    })
                    
                    position = None
                    opening_price = None
                    closing_price = None
                    position_size = 0


            # If short position is open and short_close is 1, close short position and calculate profit
            elif position == 'short':
                if any(test_strat.df.loc[i, price] < opening_price for price in ['close']):
                    stop_loss = opening_price

                if row['short1_close'] == 1:
                    if any(test_strat.df.loc[i, price] > stop_loss for price in ohlc):
                        closing_price = stop_loss

                    elif  any(test_strat.df.loc[i, price] < take_profit for price in ohlc):
                        closing_price = take_profit

                    else:
                        closing_price = row['close']

                    profit = position_size * (opening_price - closing_price)
                    capital += profit

                    positions.append({
                        'Open Time': test_strat.df['time'].iloc[i-1],
                        'Close Time': row['time'],
                        'Type': 'short',
                        'Opening Price': opening_price,
                        'Closing Price': closing_price,
                        'Take Profit': take_profit,
                        'Stop Loss': stop_loss,
                        'Profit': profit,
                        'Capital': capital
                    })
                    position = None
                    opening_price = None
                    closing_price = None
                    position_size = 0


        # Create positions dataframe
        positions_df = pd.DataFrame(positions, columns=['Open Time', 'Close Time', 'Type', 'Opening Price', 'Closing Price', 'Profit', 'Capital'])
        
    def test_runv0(self, test_strat:strategy, capital:float):
        ohlc = ['open', 'high', 'low', 'close']
        # To update
        init_capital = capital

        
        position = None
        opening_price = None
        closing_price = None
        positions = []
        position_size = 0
        fee = 0

        closing_time = None

        # To define resolution for bar
        distance = len(test_strat.df.index)
        if distance > 500000:
            resolution = 10000
        elif distance > 100000:
            resolution = 1000
        else:
            resolution = 100

        length = len(test_strat.df)
        # Loop through rows
        for row in test_strat.df.itertuples():
            
            i = row.Index
            
            if self.verbose:
                if (i % resolution) == 0:
                    print(f"{round((i/distance)*100, 3)}% COMPLETE")

            
            # If long position is possible and no position is open, open long position
            if row.long1 and row.long1 == 1 and position is None:
                position = 'long'
                opening_price = row.close
                open_time = row.close_time

                position_size = capital / opening_price
                
                fee += position_size * (0.1 / 100)

                take_profit = opening_price + (row.ATRe_21 * 6.5)
                trailing_trigger = opening_price + (row.ATRe_21 * 3.4)
                trailing_stop = opening_price + (row.ATRe_21 * 3.3)


                trailing_trigger1 = opening_price + (row.ATRe_21 * 2.2)
                trailing_stop1 = opening_price + (row.ATRe_21 * 2.1)

                trailing_trigger2 = opening_price + (row.ATRe_21 * 1.4)
                trailing_stop2 = opening_price + (row.ATRe_21 * 1.3)

                stop_loss = opening_price - (row.ATRe_21 * 0.4)

                _triggers = [
                    trailing_trigger,
                    trailing_trigger1,
                    trailing_trigger2,
                ]

                _stops = [
                    trailing_stop,
                    trailing_stop1,
                    trailing_stop2
                ]

            # If short position is possible and no position is open, open short position
            elif row.short1 and row.short1 == 1 and position is None:
                position = 'short'
                opening_price = row.close
                open_time = row.close_time

                position_size = capital / opening_price

                fee += position_size * (0.1 / 100)

                take_profit = opening_price - (row.ATRe_21 * 6.5)
                trailing_trigger = opening_price - (row.ATRe_21 * 3.4)
                trailing_stop = opening_price - (row.ATRe_21 * 3.3)

                trailing_trigger1 = opening_price - (row.ATRe_21 * 2.2)
                trailing_stop1 = opening_price - (row.ATRe_21 * 2.1)

                trailing_trigger2 = opening_price - (row.ATRe_21* 1.4)
                trailing_stop2 = opening_price - (row.ATRe_21 * 1.3)

                stop_loss = opening_price + (row.ATRe_21 * 0.075)

                _triggers = [
                    trailing_trigger,
                    trailing_trigger1,
                    trailing_trigger2,
                ]
                _stops = [
                    trailing_stop,
                    trailing_stop1,
                    trailing_stop2
                ]
            
            # If long position is open and long_close is 1, close long position and calculate profit
            elif position == 'long':
                
                if any(price < stop_loss for price in [row.open, row.high, row.low, row.close]):
                    closing_time = row.close_time
                    closing_price = stop_loss
                    fee += position_size * (0.1 / 100)
                    

                    profit = position_size * (closing_price - opening_price) - fee
                    capital += profit
                    
                    positions.append({
                        'Open Time': open_time,
                        'Close Time': closing_time,
                        'Type': 'long',
                        'Opening Price': opening_price,
                        'Closing Price': closing_price,
                        'Take Profit': take_profit,
                        'Stop Loss': stop_loss,
                        'Profit': profit,
                        'Capital': capital
                    })

                    open_time = None
                    closing_time = None
                    position = None
                    opening_price = None
                    closing_price = None
                    position_size = 0
                    fee = 0

                elif  any(price > take_profit for price in [row.open, row.high, row.low, row.close]):
                    
                    closing_time = test_strat.df.loc[i, 'close_time']
                    closing_price = take_profit
                    fee += position_size * (0.1 / 100)
                    

                    profit = position_size * (closing_price - opening_price) - fee
                    capital += profit
                                        
                    positions.append({
                        'Open Time': open_time,
                        'Close Time': closing_time,
                        'Type': 'long',
                        'Opening Price': opening_price,
                        'Closing Price': closing_price,
                        'Take Profit': take_profit,
                        'Stop Loss': stop_loss,
                        'Profit': profit,
                        'Capital': capital
                    })

                    open_time = None
                    closing_time = None
                    position = None
                    opening_price = None
                    closing_price = None
                    position_size = 0
                    fee = 0
                    closing_price = take_profit

                else:
                    for _trigger_idx in range(len(_triggers)):
                        if (test_strat.df.loc[i, "close"] > _triggers[_trigger_idx]):
                            stop_loss = _stops[_trigger_idx]
                            
            # If short position is open and short_close is 1, close short position and calculate profit
            elif position == 'short':

                if any(price > stop_loss for price in [row.open, row.high, row.low, row.close]):
                    closing_time = test_strat.df.loc[i, 'close_time']
                    closing_price = stop_loss

                    fee += position_size * (0.1 / 100)
                    capital -= fee

                    profit = position_size * (opening_price - closing_price) - fee
                    capital += profit

                    positions.append({
                        'Open Time': open_time,
                        'Close Time': closing_time,
                        'Type': 'short',
                        'Opening Price': opening_price,
                        'Closing Price': closing_price,
                        'Take Profit': take_profit,
                        'Stop Loss': stop_loss,
                        'Profit': profit,
                        'Capital': capital,
                        'Fee': fee
                    })
                    open_time = None
                    closing_time = None
                    position = None
                    opening_price = None
                    closing_price = None
                    position_size = 0
                    fee = 0
                    _triggers = []

                elif any(price < take_profit for price in [row.open, row.high, row.low, row.close]):
                    closing_time = test_strat.df.loc[i, 'close_time']
                    closing_price = take_profit


                    fee += position_size * (0.1 / 100)
                    capital -= fee

                    profit = position_size * (opening_price - closing_price) - fee
                    capital += profit

                    positions.append({
                        'Open Time': open_time,
                        'Close Time': closing_time,
                        'Type': 'short',
                        'Opening Price': opening_price,
                        'Closing Price': closing_price,
                        'Take Profit': take_profit,
                        'Stop Loss': stop_loss,
                        'Profit': profit,
                        'Capital': capital,
                        'Fee': fee
                    })
                    open_time = None
                    closing_time = None
                    position = None
                    opening_price = None
                    closing_price = None
                    position_size = 0
                    fee = 0
                    _triggers = []

                for _trigger_idx in range(len(_triggers)):
                    if (test_strat.df.loc[i, "close"] < _triggers[_trigger_idx]):
                        stop_loss = _stops[_trigger_idx]

        # Create positions dataframe
        positions_df = pd.DataFrame(positions, columns=['Open Time', 'Close Time', 'Type', 'Opening Price', 'Closing Price', 'Profit', 'Capital'])

        # TODO - eventually return this in a json and can write everything to file and give it a datetime + name
        print(line)
        print("RESULTS DATA")
        positions_df['Duration'] = (positions_df['Close Time'] - positions_df['Open Time']) / (60 * 1000)

        print(positions_df)
        # exit()
        wins = (positions_df['Profit'] > 0).sum()
        losses = (positions_df['Profit'] < 0).sum()
        start = datetime.fromtimestamp(test_strat.df['time'].iloc[0]/1000, tz=timezone.utc)
        end = datetime.fromtimestamp(test_strat.df['time'].iloc[-1]/1000, tz=timezone.utc)

        print(f"START TIME: {start.strftime('%DD/%MM/%YYYY %H:%M:%S')}")
        print(f"END TIME: {end.strftime('%DD/%MM/%YYYY %H:%M:%S')}")

        print(f"DURATION: {divmod((end-start).total_seconds(), 86400)[0]} DAYS")

        print(f"NET PROFIT: {positions_df['Profit'].sum(axis=0)}")
        print(f"PCT RETURN: {round(((positions_df['Capital'].iloc[-1] - init_capital)/init_capital)*100, 3)}")
        
        print(f"GROSS PROFIT: {positions_df.loc[positions_df['Profit'] > 0, 'Profit'].sum()}")
        print(f"GROSS LOSS: {positions_df.loc[positions_df['Profit'] < 0, 'Profit'].sum()}")
        
        print(f'WINS: {wins}')
        print(f'LOSSES: {losses}')
        print(f"WIN RATE: {round((wins / (losses + wins)) * 100, 3)}%")

        avg_win = positions_df.loc[positions_df['Profit'] > 0, 'Profit'].mean()
        avg_loss = positions_df.loc[positions_df['Profit'] < 0, 'Profit'].mean()

        print(f"MEAN WIN: {round(avg_win, 3)}")
        print(f"MEDIAN WIN: {round(positions_df.loc[positions_df['Profit'] > 0, 'Profit'].median(), 3)}")
        
        print(f"MEAN LOSS: {round(avg_loss, 3)}")
        print(f"MEDIAN LOSS: {round(positions_df.loc[positions_df['Profit'] < 0, 'Profit'].median(), 3)}")

        print(f"AVERAGE HOLDING TIME: {(positions_df['Duration']).mean()} minutes")
        print(f"AVERAGE HOLDING TIME FOR WINS: {(positions_df.loc[positions_df['Profit'] > 0, 'Duration']).mean()} minutes")
        print(f"AVERAGE HOLDING TIME FOR LOSSES: {(positions_df.loc[positions_df['Profit'] < 0, 'Duration']).mean()} minutes")

        # print(f"AVERAGER HOLDING TIME: {round(((positions_df['Close Time'] - positions_df['Open Time']).mean() / 60), 3)} minutes")

        print(f"AVG R/R: {round(avg_win/abs(avg_loss),3)}")

        print(f"MAX WIN: {positions_df.loc[positions_df['Profit'] > 0, 'Profit'].max()}")
        print(f"MAX LOSS: {positions_df.loc[positions_df['Profit'] < 0, 'Profit'].min()}")
        
        print(f"MAX DRAWDOWN PERCENT: {ta.drawdown(positions_df['Capital'])['DD_PCT'].max()}")

        print(f"BUY AND HOLD RETURN: {(test_strat.df['close'].iloc[-1] - test_strat.df['open'].iloc[0]) / test_strat.df['open'].iloc[0]}")

        print(f"SHARPE RATIO: {ta.sharpe_ratio(positions_df['Capital'], period=365)}")
        # print(f"SORTINO RATIO: {ta.sortino_ratio(positions_df['Capital'])}")
        positions_df['Returns PCT'] = positions_df['Capital'].pct_change()
        print(f"AVERAGE RETURN: {positions_df['Returns PCT'].mean()}")
        print(f"RETURNS STD DEV: {positions_df['Returns PCT'].std()}")
        print(line)

    def start_test(self, test_strat:strategy, capital:float):
        pass