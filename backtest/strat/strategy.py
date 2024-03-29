# Imports
import pandas as pd
import pandas_ta as ta
import numpy as np
from hashlib import sha256
import time
from enum import Enum
from typing import List, Dict

# Local Imports
# from backtest.strat.indicator import Indicator
from db.database import Database
# from backtest.strat.settings.settings import import_setting, Settings
# from lib.file.writer import folder_exists, create_folder, file_exists, write_json
# from lib.file.reader import get_json

class Strategy:
    """
    The strategy class is designed to encompass everything related to the strategy that I want to implement.

    At it's core, the strategy revolves around the information reltaed to the trading decisions that I would be using.
    This means that:
    - Indicators
    - Trading logic
    - Risk Management

    Are all going to be things I'd need to consider within this class.

    I might need to take in as arugments:
    - The initial Data with OHCLV
    - Orderbook data
    - Non-price related data

    We can try to adjust code to combine and separe the dataframes for performance metrics to see which is better.
    """

    def __init__(
            self, 
            # Name of the Database
            name:str="", 
            portfolio:Database=None,
            klines:List[Database]=[],
            indicators:List[Database]=[], 
            orderbook:List[Database]=[], 
            conditions:List[Database]=[],
            signals:List[Database]=[], 
            intents:Database=None, 
            positions:Database=None,
            begin_build:bool=False, # Trigger to start building all databases
            retreive:bool=False, # If we want to get the settings
            verbose:bool=False
    ): 
        self.name = name
        self.verbose = verbose

        # TODO - Not sure if this should be changed at all - seems to complex to include in the class
        
        self.portfolio = portfolio
        """
        PORTFOLIO
        """
        

        self.klines = klines
        """
        Klines
        This will hold all the things that klines hold that comes from the kline + and the 
        indicators associated with it. We do have an indicator database that holds the 
        settings for the corresponding indicators.
        """


        self.conditions = conditions
        """
        Triggers are just the the boolean versions of signals
        """
        

        self.signals = signals
        """
        Signals
        This will hold the boleans for example, if something is above another or if an 
        indicator has reached a certain level. These should be the things that specifically
        will signal that a trade should be put on. 
        """
        

        self.indicators = indicators
        """
        Indicator Settings
        Holds the settings for the indicators which will generally preside in the klines
        datbase. These include thinks like settings for EMAs and RSI etc.
        """
        

        self.intents = intents
        """
        Logic
        This involves any trading logic that needs to take place. For example if an EMA
        is above another EMA that would be under signal, there would also be a (very simple)
        piece of logic that would just open a trade. 
        """
        


        self.orderbook = orderbook
        """
        Orderbook - TODO
        Pretty self explanatory.
        """
        
        self.positions = positions
        """
        Positions - TODO
        """
        

        # Check if any of the attr is None - Return Error
        for attr, value in self.__dict__.items():
            if isinstance(value, Database) and value is [None]:
                raise ValueError(f"The attribute {attr} of type Database is None.")
            
        if begin_build:
            self.build()

    def __str__(self) -> str:
        return f"STRATEGY >> Name: {self.name} "
    
    @property
    def df_columns(self) -> Dict[str, list]:
        """
        Returns:
        Dict(
            str(Name of Dataframe): [List of Dataframe columns]
        )
        """
        
        ret_data = {}
        
        for kline_db in self.klines:
            if kline_db.df:
                new_col_list = kline_db.df.columns.tolist()
                ret_data[f"{kline_db.name}"] = new_col_list
            else:
                ret_data[f"{kline_db.name}"] = []
        return ret_data

    # TODO - create representation
    def __repr__(self) -> str:
        
        return f""

    def build(self):
        """
        This function builds all the required database to return their corresponding dataframes.
        In doing so, you can then start to either backtest or perform the strategy accordingly.
        """
        # Build klines
        for kline_db in self.klines:
            
            kline_db.build()
            print(f"INTERVAL: {kline_db.arguments['interval']}")
            
            for indicator_db in self.indicators:
                
                if indicator_db.arguments['interval'][0] == kline_db.arguments['interval']:
                
                    kline_db.df = indicator_db.build(
                        indicator_list=indicator_db.arguments['indicators'],
                        df=kline_db.df
                    )
            
            """
            Triggers, are now changed so that they're not calculated for the entire
            dataframe, but they are checked on the fly
            """

            # for trigger in self.triggers.arguments['triggers']:
            #     kline_db.df = trigger.build_trigger(df=kline_db.df)

            if self.verbose:
                print("------------------------------ DATAFRAME ------------------------------")
                print(kline_db.df)

        

    def backtest(self):
        pass
        
    def save(self):
        if self.verbose:
            print("SAVING...")
    
    def backtest(self):
        pass
        

    def go_live(self):
        pass
        