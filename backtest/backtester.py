# Imports
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timezone
from hashlib import sha256
import time
import numpy as np

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
        
    def test_runv0(self, test_strat:strategy, capital:float):
        settings_string = str(test_strat.indicator_settings_list)
        settings_hash = sha256(settings_string.encode()).hexdigest()
        
        filepath = f'db/strategies/results/'

        # Create folder if it doesn't exist
        # if not folder_exists(settings_hash, filepath):
        #     create_folder(settings_hash, filepath)
        # else:
        #     results = get_json(
        #         f"{filepath}{settings_hash}/results.json"
        #     )
        #     for x in results.keys():
        #         print(f"{x} // {results[x]}")
        #     return None


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

        # Loop through rows
        for row in test_strat.df.itertuples():

            # print(row)
            
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

                take_profit = opening_price + (row.ATRe_21 * 2)
                trailing_trigger = opening_price + (row.ATRe_21 * 1.6)
                trailing_stop = opening_price + (row.ATRe_21 * 1.4)


                trailing_trigger1 = opening_price + (row.ATRe_21 * 1.4)
                trailing_stop1 = opening_price + (row.ATRe_21 * 1.3)

                trailing_trigger2 = opening_price + (row.ATRe_21 * 1.3)
                trailing_stop2 = opening_price + (row.ATRe_21 * 1.1)

                trailing_trigger3 = opening_price + (row.ATRe_21 * 1)
                trailing_stop3 = opening_price + (row.ATRe_21 * 0.5)


                stop_loss = opening_price - (row.ATRe_21 * 0.2)

                _triggers = [
                    trailing_trigger,
                    trailing_trigger1,
                    trailing_trigger2,
                    trailing_trigger3,
                    # trailing_trigger4
                ]

                _stops = [
                    trailing_stop,
                    trailing_stop1,
                    trailing_stop2,
                    trailing_stop3,
                    # trailing_stop4
                ]

            # If short position is possible and no position is open, open short position
            elif row.short1 and row.short1 == 1 and position is None:
                position = 'short'
                opening_price = row.close
                open_time = row.close_time

                position_size = capital / opening_price

                fee += position_size * (0.1 / 100)

                take_profit = opening_price - (row.ATRe_21 * 2)
                trailing_trigger = opening_price - (row.ATRe_21 * 1.6)
                trailing_stop = opening_price - (row.ATRe_21 * 1.4)

                trailing_trigger1 = opening_price - (row.ATRe_21 * 1.4)
                trailing_stop1 = opening_price - (row.ATRe_21 * 1.3)

                trailing_trigger2 = opening_price - (row.ATRe_21* 1.3)
                trailing_stop2 = opening_price - (row.ATRe_21 * 1.1)

                trailing_trigger3 = opening_price - (row.ATRe_21 * 0.9)
                trailing_stop3 = opening_price - (row.ATRe_21 * 0.8)

                stop_loss = opening_price + (row.ATRe_21 * 0.2)

                _triggers = [
                    trailing_trigger,
                    trailing_trigger1,
                    trailing_trigger2,
                    trailing_trigger3,
                    # trailing_trigger4
                ]
                _stops = [
                    trailing_stop,
                    trailing_stop1,
                    trailing_stop2,
                    trailing_stop3,
                    # trailing_stop4
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
        
        positions_df['Duration'] = (positions_df['Close Time'] - positions_df['Open Time']) / (60 * 1000)
        
        """

        We now try to create all the data that we look for and add that into a hashed header to be added into a JSON
        
        """

        wins = (positions_df['Profit'] > 0).sum()
        losses = (positions_df['Profit'] < 0).sum()
        start = datetime.fromtimestamp(test_strat.df['time'].iloc[0]/1000, tz=timezone.utc)
        end = datetime.fromtimestamp(test_strat.df['time'].iloc[-1]/1000, tz=timezone.utc)
        positions_df['Returns PCT'] = positions_df['Capital'].pct_change()
        avg_win = positions_df.loc[positions_df['Profit'] > 0, 'Profit'].mean()
        avg_loss = positions_df.loc[positions_df['Profit'] < 0, 'Profit'].mean()
        lastupdate = int(time.time())

        result = {
            "lastupdate": lastupdate,
            "starttime": start.strftime('%DD/%MM/%YYYY %H:%M:%S'),
            "endtime": end.strftime('%DD/%MM/%YYYY %H:%M:%S'),
            "days": divmod((end-start).total_seconds(), 86400)[0],
            "netprofit": positions_df['Profit'].sum(axis=0),
            "return_pct": round(((positions_df['Capital'].iloc[-1] - init_capital)/init_capital)*100, 3),
            "grossprofit": positions_df.loc[positions_df['Profit'] > 0, 'Profit'].sum(),
            "grossloss": positions_df.loc[positions_df['Profit'] < 0, 'Profit'].sum(),
            "wins": wins,
            "losses": losses,
            "winrate": round((wins / (losses + wins)) * 100, 3),
            "meanwin": positions_df.loc[positions_df['Profit'] > 0, 'Profit'].mean(),
            "medianwin": round(positions_df.loc[positions_df['Profit'] > 0, 'Profit'].median(), 3),
            "meanholdingtime": (positions_df['Duration']).mean(),
            "meanwinholdingtime": (positions_df.loc[positions_df['Profit'] > 0, 'Duration']).mean(),
            "meanlossholdingtime": (positions_df.loc[positions_df['Profit'] < 0, 'Duration']).mean(),
            "averagerr": round(avg_win/abs(avg_loss),3),
            "maxwin": positions_df.loc[positions_df['Profit'] > 0, 'Profit'].max(),
            "maxloss": positions_df.loc[positions_df['Profit'] < 0, 'Profit'].max(),
            "maxdrawdown_pct": ta.drawdown(positions_df['Capital'])['DD_PCT'].max(),
            "hodlreturn": (test_strat.df['close'].iloc[-1] - test_strat.df['open'].iloc[0]) / test_strat.df['open'].iloc[0],
            "sharpe": ta.sharpe_ratio(positions_df['Capital'], period=365),
            "meanreturn": positions_df['Returns PCT'].mean(),
            "return_stdev": positions_df['Returns PCT'].std()
        }

        
        # Quick hack to convert floats
        for x in result.keys():
            result[x] = str(result[x])

        # Write the results in this folder
        write_json(
            result,
            "results.json",
            filepath+settings_hash+"/"
        )
        
    def test_runv1(self, test_strat:strategy, capital:float):
        settings_string = str(test_strat.indicator_settings_list)
        settings_hash = sha256(settings_string.encode()).hexdigest()
        
        filepath = f'db/strategies/results/'

        # Create folder if it doesn't exist
        if not folder_exists(settings_hash, filepath):
            create_folder(settings_hash, filepath)
        # else:
        #     results = get_json(
        #         f"{filepath}{settings_hash}/results.json"
        #     )
        #     for x in results.keys():
        #         print(f"{x} // {results[x]}")
        #     return None

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

                take_profit = opening_price + (row.ATRe_21 * 2)
                trailing_trigger = opening_price + (row.ATRe_21 * 1.6)
                trailing_stop = opening_price + (row.ATRe_21 * 1.4)


                trailing_trigger1 = opening_price + (row.ATRe_21 * 1.4)
                trailing_stop1 = opening_price + (row.ATRe_21 * 1.3)

                trailing_trigger2 = opening_price + (row.ATRe_21 * 1.3)
                trailing_stop2 = opening_price + (row.ATRe_21 * 1.1)

                trailing_trigger3 = opening_price + (row.ATRe_21 * 1)
                trailing_stop3 = opening_price + (row.ATRe_21 * 0.5)


                stop_loss = opening_price - (row.ATRe_21 * 0.2)

                _triggers = [
                    trailing_trigger,
                    trailing_trigger1,
                    trailing_trigger2,
                    trailing_trigger3,
                    # trailing_trigger4
                ]

                _stops = [
                    trailing_stop,
                    trailing_stop1,
                    trailing_stop2,
                    trailing_stop3,
                    # trailing_stop4
                ]

            # If short position is possible and no position is open, open short position
            elif row.short1 and row.short1 == 1 and position is None:
                position = 'short'
                opening_price = row.close
                open_time = row.close_time

                position_size = capital / opening_price

                fee += position_size * (0.1 / 100)

                take_profit = opening_price - (row.ATRe_21 * 2)
                trailing_trigger = opening_price - (row.ATRe_21 * 1.6)
                trailing_stop = opening_price - (row.ATRe_21 * 1.4)

                trailing_trigger1 = opening_price - (row.ATRe_21 * 1.4)
                trailing_stop1 = opening_price - (row.ATRe_21 * 1.3)

                trailing_trigger2 = opening_price - (row.ATRe_21* 1.3)
                trailing_stop2 = opening_price - (row.ATRe_21 * 1.1)

                trailing_trigger3 = opening_price - (row.ATRe_21 * 0.9)
                trailing_stop3 = opening_price - (row.ATRe_21 * 0.8)

                stop_loss = opening_price + (row.ATRe_21 * 0.2)

                _triggers = [
                    trailing_trigger,
                    trailing_trigger1,
                    trailing_trigger2,
                    trailing_trigger3,
                    # trailing_trigger4
                ]
                _stops = [
                    trailing_stop,
                    trailing_stop1,
                    trailing_stop2,
                    trailing_stop3,
                    # trailing_stop4
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
        
        positions_df['Duration'] = (positions_df['Close Time'] - positions_df['Open Time']) / (60 * 1000)
        
        """

        We now try to create all the data that we look for and add that into a hashed header to be added into a JSON
        
        """

        wins = (positions_df['Profit'] > 0).sum()
        losses = (positions_df['Profit'] < 0).sum()
        start = datetime.fromtimestamp(test_strat.df['time'].iloc[0]/1000, tz=timezone.utc)
        end = datetime.fromtimestamp(test_strat.df['time'].iloc[-1]/1000, tz=timezone.utc)
        positions_df['Returns PCT'] = positions_df['Capital'].pct_change()
        avg_win = positions_df.loc[positions_df['Profit'] > 0, 'Profit'].mean()
        avg_loss = positions_df.loc[positions_df['Profit'] < 0, 'Profit'].mean()
        lastupdate = int(time.time())

        result = {
            "lastupdate": lastupdate,
            "starttime": start.strftime('%DD/%MM/%YYYY %H:%M:%S'),
            "endtime": end.strftime('%DD/%MM/%YYYY %H:%M:%S'),
            "days": divmod((end-start).total_seconds(), 86400)[0],
            "netprofit": positions_df['Profit'].sum(axis=0),
            "return_pct": round(((positions_df['Capital'].iloc[-1] - init_capital)/init_capital)*100, 3),
            "grossprofit": positions_df.loc[positions_df['Profit'] > 0, 'Profit'].sum(),
            "grossloss": positions_df.loc[positions_df['Profit'] < 0, 'Profit'].sum(),
            "wins": wins,
            "losses": losses,
            "winrate": round((wins / (losses + wins)) * 100, 3),
            "meanwin": positions_df.loc[positions_df['Profit'] > 0, 'Profit'].mean(),
            "medianwin": round(positions_df.loc[positions_df['Profit'] > 0, 'Profit'].median(), 3),
            "meanholdingtime": (positions_df['Duration']).mean(),
            "meanwinholdingtime": (positions_df.loc[positions_df['Profit'] > 0, 'Duration']).mean(),
            "meanlossholdingtime": (positions_df.loc[positions_df['Profit'] < 0, 'Duration']).mean(),
            "averagerr": round(avg_win/abs(avg_loss),3),
            "maxwin": positions_df.loc[positions_df['Profit'] > 0, 'Profit'].max(),
            "maxloss": positions_df.loc[positions_df['Profit'] < 0, 'Profit'].max(),
            "maxdrawdown_pct": ta.drawdown(positions_df['Capital'])['DD_PCT'].max(),
            "hodlreturn": (test_strat.df['close'].iloc[-1] - test_strat.df['open'].iloc[0]) / test_strat.df['open'].iloc[0],
            "sharpe": ta.sharpe_ratio(positions_df['Capital'], period=365),
            "meanreturn": positions_df['Returns PCT'].mean(),
            "return_stdev": positions_df['Returns PCT'].std()
        }

        
        # Quick hack to convert floats
        for x in result.keys():
            result[x] = str(result[x])

        # Write the results in this folder
        write_json(
            result,
            "results.json",
            filepath+settings_hash+"/"
        )
        
