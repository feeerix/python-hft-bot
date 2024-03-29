# Imports
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timezone
from hashlib import sha256
import time
import numpy as np
from typing import List
from dataclasses import fields

# Local Imports
# from lib.api.binance.interface import Binance
from lib.file.writer import *
from lib.file.reader import *

# from db.database import Database

# from backtest.strat.indicator import Indicator
from backtest.strat.settings.settings import Settings
from backtest.strat.strategy import Strategy
from backtest.position import *

from lib.cli.printer import line

class Backtester:
    def __init__(self, verbose:bool=False):
        
        self.db = None
        self.strategy = None
        self.verbose = verbose

    """
    Single asset backtest - USD
    """
    def backtest(self, strategies:List[Strategy], capital:float):
        current_position = None
        opening_price = None
        closing_price = None
        positions = []
        position_size = 0
        init_capital = capital

        # print(strategies.intents.build())
        pos_type_list = []
        for pos_logic in strategies.intents.arguments['logic']:
            pos_type_list.append(
                pos_logic.settings.arguments.pos_family
            )
        
        for df_index in range(len(strategies.klines)):
            distance = len(strategies.klines[df_index].df)
            # To be adjusted
            if distance > 500000:
                resolution = 10000
            elif distance > 100000:
                resolution = 1000
            else:
                resolution = 100

            """
            First we want to get all the position types we want to enter
            and their conditions. 
            """

            # print(strategies) # Strategies
            # print(strategies.intents) # DB of intents
            # print(strategies.intents.arguments) # list of intent classes under logic
            # print(strategies.intents.arguments['logic']) # List of intent clases (list of each intent for positions)
            # for pos_logic in strategies.intents.arguments['logic']: # For each position type
            #     print(pos_logic) # each intent class
            #     print(pos_logic.settings) # Intent settings
            #     print(pos_logic.settings.columns) # The column containing other info

            #     for condition in pos_logic.settings.columns['conditions'].keys():
            #         condition.execute_behavior(
            #             condition_settings=pos_logic.settings.columns['conditions'][condition],
            #             condition_value=pos_logic.settings.columns['values']
            #         )

            """
            At the moment, this will imply a time based and candled based system. The reason
            for doing this at the moment would be that we want to include all the candles with 
            which we want to make decisions. 

            This will also be the way we want to integrate websocket eventually, so 
            is part of the reason why we might think about keeping this at the moment.

            """
            current_values = ConditionValues()

            for row_idx in range(len(strategies.klines[df_index].df)):
            # for row in strategies.klines[df_index].df.itertuples():
                # Row - index
                # i = row.Index

                """
                TODO - to add a better capital management system of some sort.
                """
                # if capital < 0:
                #     print("You went broke!")
                #     break

                """
                TODO -  is there a better logging system that doesn't interfere with 
                the for loop per line?
                """

                if self.verbose:
                    if (row_idx % resolution) == 0:
                        print(f"{round((row_idx/distance)*100, 3)}% COMPLETE")
                
                """
                At this point, we're going to look through all of the intents,
                via:
                strategies.intents - and call the "check" function
                to see if we're still looking for this position based on 
                the specific conditions in the function.
                """
                
                # for pos_type in strategies.intents.arguments['logic']:
                #     """
                #     For each position type:
                #     """
                #     print(f"pos_type {pos_type}")
                #     for conditionBlock in strategies.conditions.arguments['blocks']:
                #         for positionCondition in conditionBlock.arguments.keys():
                #             """
                #             For each one of the settings:
                #             """
                #             if positionCondition == pos_type.settings.func_name:
                #                 print(current_values.NUMBER)
                #                 print(conditionBlock.arguments[positionCondition])
                #                 if not conditionBlock.func_name.check_behavior(
                #                     condition_value=current_values.NUMBER,
                #                     condition_setting=conditionBlock.arguments[positionCondition]
                #                 ):
                                
                #                     print("break")
                #                     break

                            # if positionCondition == pos_type

                    # for f in fields(pos_type.settings.columns['settings']):
                    #     print(f"{f.name} // {getattr(current_values, f.name)}")
                    #     print(f"Settings: {f.name} // {getattr(pos_type.settings.columns['settings'], f.name)}")

                    # print(strategies.conditions.arguments['blocks'][0].arguments)
                    # print(strategies.conditions.arguments['blocks'])
                
                    # for condition in 

                if current_position is None:
                    """
                    TODO - adjust this to include the correspoding logic for 
                    PositionType, ConditionBlocks, ConditionValues.

                    If you've passed the above if statement, you currently don't
                    have a position in place, at all. We will need to change this
                    to be a check - for that we have maxed the amount of risk.
                    """
                    for pos_logic in strategies.intents.arguments['logic']:
                        # We have found a place where we might be able to make a transaction
                        if pos_logic.check(strategies.klines[df_index].df, row_idx):
                            print("VALID!! ------------")
                            
                            # print(current_values)
                            # for conditionBlock in strategies.conditions.arguments['blocks']:
                            #     for positionCondition in conditionBlock.arguments.keys():
                                    
                            #         print(conditionBlock)
                            #         print(positionCondition)
                            #         exit()

                            # If verbose
                            """
                            TODO
                            BE ABLE TO MAKE A POSITION CLASS WITH A FACTORY
                            Think about creating a Position class factory that can
                            create all the lists of Trades based on simplified terms

                            Let's create a Trade for now, so I can get this up and running.
                            Additionally, we'll some assumptions about the trade, being we'll
                            use the close of the previous candle to open the trade
                            and get an full fill.
                            """

                            print(f"-- CREATING POSITION --")
                            print(f"POS LOGIC: {pos_logic}")
                            print(f"POSITION TYPE: {pos_logic.settings.func_name}")
                            print(f"CURRENT POSITIONS OPEN: {current_values.NUMBER}")
                            print(f"MAX POSITIONS OPEN: {strategies.conditions.arguments['blocks'][0].arguments[pos_logic.settings.func_name]}")
                            print(f"CLOSE: {strategies.klines[df_index].df.loc[row_idx].close}")
                            print(f"EXPECTED ENTRY: {strategies.klines[df_index].df.loc[row_idx].close}")
                            print(f"ACTUAL ENTRY: AUTO")
                            print(f"INIT CAPITAL: {init_capital}")
                            print(f"CURRENT CAPITAL: {capital}")
                            print(f"EXPECTED RISK: {strategies.conditions.arguments['blocks'][1].arguments[pos_logic.settings.func_name]}")
                            print(f"EXPECTED TP {pos_logic.settings.arguments.close_style}")
                            print(strategies.conditions.arguments['blocks'][0].arguments)

                            # print(f"EXPECTED RISK: {}")
                            # print(f"EXPECTED AMOUNT: {}")
                            # print(f"ACTUAL FILL")

                            exit()
                            if self.verbose:
                                print("CREATING POSITION")
                                # PositionType
                                print(f"POS_TYPE: {pos_logic.settings.func_name}")
                                # 
                                print(f"NEW CURRENT POSITION NAME: {current_position}")
                                
                            exit()
                
                
                # print(strategies[0].logic.name)
                
                # # Looking for new position
                # if current_position is None:
                #     # Cycle every position type (long/short/arb) etc
                #     for pos_type in test_strat.position_condition_settings.keys():
                #         # For every type of position that we're trying to open (could be high risk long or short term for example)
                #         for idx in range(len(test_strat.position_condition_settings[pos_type])):

                #             # Get the name of the position
                #             pos_name = test_strat.position_condition_settings[pos_type][idx]['name']
                            
                #             # if the position type exist and we are ready to open a position
                #             if getattr(row, pos_name) and (getattr(row, pos_name) == 1):
                                
                #                 # If verbose
                #                 if self.verbose:
                #                     print(f"POS_TYPE: {pos_type}")
                #                     print(f"CURRENT POSITION: {position}")
                #                     print("CREATING POSITION")
                #                     print(f"POS_NAME: {pos_name}")
                                
                #                 short_inverse = 1
                #                 # If short we inverse
                #                 if pos_type == 'short':
                #                     # We are short - inverse
                #                     position_type = PositionType.SHORT
                #                     short_inverse = -1
                                
                #                 # Get position type
                #                 position = pos_type
                                
                #                 # TODO - make sure we can update set arbitrary opening price
                #                 opening_price = row.close

                #                 # TODO - make sure we can set arbitrary opening time (within )
                #                 open_time = row.close_time
                #                 position_size = capital / opening_price

                #                 # TODO - make sure we can select maker or taker fee (or even custom fee) via the settings
                #                 fee += position_size * (maker_fee / 100)

                #                 # TODO - make sure we can have an arbitrary number of trailing stops
                #                 atr = getattr(row, "ATRe_21")
                #                 take_profit = opening_price + (atr * 1.8 * short_inverse)
                #                 trailing_trigger = opening_price + (atr * 1.6 * short_inverse)
                #                 trailing_stop = opening_price + (atr * 1.4 * short_inverse)


                #                 trailing_trigger1 = opening_price + (atr * 1.4 * short_inverse)
                #                 trailing_stop1 = opening_price + (atr * 1.3 * short_inverse)

                #                 trailing_trigger2 = opening_price + (atr * 1.3 * short_inverse)
                #                 trailing_stop2 = opening_price + (atr * 1.1 * short_inverse)

                #                 trailing_trigger3 = opening_price + (atr * 1 * short_inverse)
                #                 trailing_stop3 = opening_price + (atr * 0.5 * short_inverse)

                #                 stop_loss = opening_price - (atr * 0.2 * short_inverse)

                #                 _triggers = [
                #                     trailing_trigger,
                #                     trailing_trigger1,
                #                     trailing_trigger2,
                #                     trailing_trigger3,
                #                     # trailing_trigger4
                #                 ]

                #                 _stops = [
                #                     trailing_stop,
                #                     trailing_stop1,
                #                     trailing_stop2,
                #                     trailing_stop3,
                #                     # trailing_stop4
                #                 ]

                #                 # ---------------------------------------------------


    def test_run(self, test_strat:Strategy, capital:float):
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
        
    def test_runv0(self, test_strat:Strategy, capital:float, run_settings:Settings=None, exchange_settings:Settings=None, settings_write:bool=False):
        # filepath to save strategies
        filepath = f'db/strategies/results/'

        # Maker and taker fees to be used when necessary
        maker_fee = exchange_settings.data['arguments']['maker_fee']
        taker_fee = exchange_settings.data['arguments']['taker_fee']

        # TODO - update the writing settings
        if settings_write:
            settings_string = str(test_strat.indicator_settings_list)
            settings_hash = sha256(settings_string.encode()).hexdigest()

            # Create folder if it doesn't exist
            if not folder_exists(settings_hash, filepath):
                create_folder(settings_hash, filepath)
            else:
                print(f"\'{settings_hash}\' folder exists.")

                # Prints the previous results - NOTE it does not consider the timeframe and starttime/endtime of the backtest
                test_json = get_json(f"{filepath}{settings_hash}/results.json")
                print(test_json)
                return None

        ohlc = ['open', 'high', 'low', 'close']
        
        # To update
        init_capital = capital
        
        # All general settings to 0 when starting backtest
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
            resolution = 100000
        elif distance > 100000:
            resolution = 10000
        else:
            resolution = 1000

        print("POSITION CONDITION SETTINGS")
        print(test_strat.position_condition_settings)
        
        # Loop through all the rows
        for row in test_strat.df.itertuples():
            
            # Row - index
            i = row.Index

            # Get a list of all OHLC
            row_price =  [getattr(row, key) for key in ohlc]

            if self.verbose:
                if (i % resolution) == 0:
                    print(f"-- {i} --")
                    print(f"{round((i/distance)*100, 3)}% COMPLETE")

            # If there is no existing position
            if position is None:
                
                # Cycle every position type (long/short/arb) etc
                for pos_type in test_strat.position_condition_settings.keys():
                    
                    # For every type of position that we're trying to open (could be high risk long or short term for example)
                    for idx in range(len(test_strat.position_condition_settings[pos_type])):

                        # Get the name of the position
                        pos_name = test_strat.position_condition_settings[pos_type][idx]['name']
                        
                        # if the position type exist and we are ready to open a position
                        if getattr(row, pos_name) and (getattr(row, pos_name) == 1):
                            
                            # If verbose
                            if self.verbose:
                                print(f"POS_TYPE: {pos_type}")
                                print(f"CURRENT POSITION: {position}")
                                print("CREATING POSITION")
                                print(f"POS_NAME: {pos_name}")
                            
                            short_inverse = 1
                            # If short we inverse
                            if pos_type == 'short':
                                # We are short - inverse
                                position_type = PositionType.SHORT
                                short_inverse = -1
                            
                            # Get position type
                            position = pos_type
                            
                            # TODO - make sure we can update set arbitrary opening price
                            opening_price = row.close

                            # TODO - make sure we can set arbitrary opening time (within )
                            open_time = row.close_time
                            position_size = capital / opening_price

                            # TODO - make sure we can select maker or taker fee (or even custom fee) via the settings
                            fee += position_size * (maker_fee / 100)

                            # TODO - make sure we can have an arbitrary number of trailing stops
                            atr = getattr(row, "ATRe_21")
                            take_profit = opening_price + (atr * 1.8 * short_inverse)
                            trailing_trigger = opening_price + (atr * 1.6 * short_inverse)
                            trailing_stop = opening_price + (atr * 1.4 * short_inverse)


                            trailing_trigger1 = opening_price + (atr * 1.4 * short_inverse)
                            trailing_stop1 = opening_price + (atr * 1.3 * short_inverse)

                            trailing_trigger2 = opening_price + (atr * 1.3 * short_inverse)
                            trailing_stop2 = opening_price + (atr * 1.1 * short_inverse)

                            trailing_trigger3 = opening_price + (atr * 1 * short_inverse)
                            trailing_stop3 = opening_price + (atr * 0.5 * short_inverse)

                            stop_loss = opening_price - (atr * 0.2 * short_inverse)

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

                            # ---------------------------------------------------
            
            # TODO - consider how we can update this to be more performant
            elif position == "long":
                    if any(price < stop_loss for price in row_price):

                        if self.verbose:
                            print("-- STOPLOSS HIT! --")

                        closing_time = row.close_time
                        closing_price = stop_loss
                        fee += position_size * (maker_fee / 100)
                        

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

                        print(position)

                        open_time = None
                        closing_time = None
                        position = None
                        opening_price = None
                        closing_price = None
                        position_size = 0
                        fee = 0



                        exit()

                    elif any(price > take_profit for price in row_price):
                    
                        closing_time = test_strat.df.loc[i, 'close_time']
                        closing_price = take_profit
                        fee += position_size * (maker_fee / 100)
                        
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

                        exit()

                    else:
                        for _trigger_idx in range(len(_triggers)):
                            if (test_strat.df.loc[i, "close"] > _triggers[_trigger_idx]):
                                stop_loss = _stops[_trigger_idx]

            elif position == "short":
                if any(price > stop_loss for price in row_price):
                    
                    if self.verbose:
                        print("-- STOPLOSS HIT! --")

                    closing_time = test_strat.df.loc[i, 'close_time']
                    closing_price = stop_loss

                    fee += position_size * (maker_fee / 100)
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

                    exit()

            
                elif any(price < take_profit for price in row_price):
                    closing_time = test_strat.df.loc[i, 'close_time']
                    closing_price = take_profit


                    fee += position_size * (maker_fee / 100)
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

                    exit()

                for _trigger_idx in range(len(_triggers)):
                    if (test_strat.df.loc[i, "close"] < _triggers[_trigger_idx]):
                        stop_loss = _stops[_trigger_idx]
                    
        # Create positions dataframe
        positions_df = pd.DataFrame(positions, columns=['Open Time', 'Close Time', 'Type', 'Opening Price', 'Closing Price', 'Profit', 'Capital'])

        # TODO - eventually return this in a json and can write everything to file and give it a datetime + name
        print(line)
        print("RESULTS DATA")
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

        
        print(result)
        if settings_write:
            # Quick hack to convert floats
            for x in result.keys():
                result[x] = str(result[x])

            # Write the results in this folder
            write_json(
                result,
                "results.json",
                filepath+settings_hash+"/"
            )
        print("END")

    def test_runv0a(self, test_strat:Strategy, capital:float, run_settings:Settings=None, exchange_settings:Settings=None, settings_write:bool=False):
        # filepath to save strategies
        filepath = f'db/strategies/results/'

        # Maker and taker fees to be used when necessary
        maker_fee = exchange_settings.data['arguments']['maker_fee']
        taker_fee = exchange_settings.data['arguments']['taker_fee']

        ohlc = ['open', 'high', 'low', 'close']
        
        # To update
        init_capital = capital
        
        # All general settings to 0 when starting backtest
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
            resolution = 100000
        elif distance > 100000:
            resolution = 10000
        else:
            resolution = 1000

        print("POSITION CONDITION SETTINGS")
        print(test_strat.position_condition_settings)
        # exit()
        # Loop through all the rows
        print(test_strat.df.columns.to_list())
        for row in test_strat.df.itertuples():
            
            # Row - index
            i = row.Index

            # Get a list of all OHLC
            # row_price =  [getattr(row, key) for key in ohlc]
            if row.long1 and row.long1 == 1:
                
                exit()

            if self.verbose:
                if (i % resolution) == 0:
                    print(f"-- {i} --")
                    print(f"{round((i/distance)*100, 3)}% COMPLETE")

    def compute_results(self, positions_df:pd.DataFrame, df:pd.DataFrame, init_capital: int):
        # Create positions dataframe
        # positions_df = pd.DataFrame(positions, columns=['Open Time', 'Close Time', 'Type', 'Opening Price', 'Closing Price', 'Profit', 'Capital'])

        # TODO - eventually return this in a json and can write everything to file and give it a datetime + name
        positions_df['Duration'] = (positions_df['Close Time'] - positions_df['Open Time']) / (60 * 1000)
        
        """

        We now try to create all the data that we look for and add that into a hashed header to be added into a JSON
        
        """

        wins = (positions_df['Profit'] > 0).sum()
        losses = (positions_df['Profit'] < 0).sum()
        start = datetime.fromtimestamp(df['time'].iloc[0]/1000, tz=timezone.utc)
        end = datetime.fromtimestamp(df['time'].iloc[-1]/1000, tz=timezone.utc)
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
            "hodlreturn": (df['close'].iloc[-1] - df['open'].iloc[0]) / df['open'].iloc[0],
            "sharpe": ta.sharpe_ratio(positions_df['Capital'], period=365),
            "meanreturn": positions_df['Returns PCT'].mean(),
            "return_stdev": positions_df['Returns PCT'].std()
        }

        
        print(result)