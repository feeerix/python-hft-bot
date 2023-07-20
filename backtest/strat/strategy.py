# Imports
import pandas as pd
import pandas_ta as ta
import numpy as np
from hashlib import sha256
import time
from enum import Enum

# Local Imports
from backtest.strat.indicator import Indicator
from db.database import Database
from backtest.strat.settings.settings import import_setting, Settings
from lib.file.writer import folder_exists, create_folder, file_exists, write_json
from lib.file.reader import get_json

class _Strategy:
    """
    The strategy class is designed to encompass everything related to the strategy that I want to implement.
    """

    def __init__(self, name:str, df:pd.DataFrame, verbose:bool=False, retreive:bool=False): 
        self.name = name
        self.verbose = verbose
        self.df = None

        # ------------------
        # indicator_example = [
        #     {
        #         indicator.settings.data
        #     }, ...
        # ]

        self.indicator_settings_list = []
        self.position_condition_settings = {
            "long": [],
            "short": []
        }
        
        # Initialise the DF
        self.init_df(df)

        if retreive:
            # Get the settings from JSON based on name
            self.get_settings()

            # Add the indicators based on settings        
            for indicator_setting in self.indicator_settings_list:
                new_setting = import_setting(indicator_setting)
                self.add_indicator(Indicator(new_setting), recording=False)

            # Add he position requirements based on settings
            for position_type in self.position_condition_settings.keys():
                
                for position_setting in self.position_condition_settings[position_type]:
                    
                    new_setting = import_setting(position_setting)
                    self.add_entry(new_setting, recording=False)

        # ------------------

    # Initialise DF
    def init_df(self, df:pd.DataFrame):
        # Set up the dataframe
        self.df = df

    # Add indicator to self.df
    def add_indicator(self, _indicator:Indicator, recording:bool=True):
        if self.verbose:
            print(_indicator.settings.data)

        # If we want to write the settings
        if recording:
            self.indicator_settings_list.append(_indicator.settings.data)

        # Add individual indicator
        self.df = pd.concat(
            [
                self.df, # Existing DF
                _indicator.ret_indicator(self.df)
            ], # New DF
            axis=1, 
            # ignore_index=True # -> removed index
        )

    # Add entry conditions
    def add_entry(self, _settings:Settings, recording:bool=True):
        # Test print
        if self.verbose:
            print(_settings.data)
            
        if recording:
            for pos_type in self.position_condition_settings.keys():

                if pos_type == _settings.data["func_name"]:
                    self.position_condition_settings[pos_type].append(
                        _settings.data
                    )
            # print(_settings.data['arguments']['open'][True])
            # print(self.df.columns.to_list())
            # print(self.df[_settings.data['arguments']['open'][True]])
            # exit()
            self.df[_settings.data['name']] = np.where((
                    (self.df[_settings.data['arguments']['open'][True]].all(axis=1)) &
                    (self.df[_settings.data['arguments']['open'][False]].sum(axis=1) == 0)
            ), 1, 0)
        else:
            self.df[_settings.data['name']] = np.where((
                    (self.df[_settings.data['arguments']['open']['true']].all(axis=1)) &
                    (self.df[_settings.data['arguments']['open']['false']].sum(axis=1) == 0)
            ), 1, 0)

    # Add close conditions
    def add_close(self, _settings:Settings, recording:bool=True):    
        # Test print
        if self.verbose:
            print(_settings.data)
        

        if recording:
            for pos_type in self.position_condition_settings.keys():

                if pos_type == _settings.data["func_name"]:
                    self.position_condition_settings[pos_type].append(
                        _settings.data
                    )
            
            self.df[_settings.data['name']] = np.where((
                    (self.df[_settings.data['arguments']['close'][True]].all(axis=1)) &
                    (self.df[_settings.data['arguments']['close'][False]].sum(axis=1) == 0)
            ), 1, 0)
            
        else:
            self.df[_settings.data['name']] = np.where((
                    (self.df[_settings.data['arguments']['close']['true']].all(axis=1)) &
                    (self.df[_settings.data['arguments']['close']['false']].sum(axis=1) == 0)
            ), 1, 0)
    
    # Write Settings to file
    def write_settings(self):
        strat_folder = f'db/strategies/settings/'
        if not folder_exists(self.name, strat_folder):
            create_folder(self.name, strat_folder)
        
        """
        Hashing the settings

        We hash the indicator and the position seperately and add our own prefix to it.

        We check if this has been completed already.

        """
        indicator_hash = "indi-"+sha256(str(self.indicator_settings_list).encode()).hexdigest()
        position_hash = "posi-"+sha256(str(self.position_condition_settings).encode()).hexdigest()
        
        # lastupdate = 
        lastupdate = int(time.time())

        write_json(
            {
                "indicator_hash": indicator_hash,
                "position_hash": position_hash,
                "lastupdate": lastupdate,
                'result_headers': []
            },
            'headers.json',
            strat_folder+self.name+'/'
        )
        

        write_json(
            self.indicator_settings_list,
            'indicator_settings.json',
            strat_folder+self.name+'/'
        )

        write_json(
            self.position_condition_settings,
            'position_settings.json',
            strat_folder+self.name+'/'
        )

    # Get settings from file via name
    def get_settings(self, settings_id:str):
        strat_folder = f'db/strategies/settings/'

        self.indicator_settings_list = get_json(f"{strat_folder}{self.name}/indicator_settings.json")
        self.position_condition_settings = get_json(f"{strat_folder}{self.name}/position_settings.json")
        
        if self.verbose:
            print("Position Settings")
            print(self.position_condition_settings)
            print("Indicator Settings")
            print(self.indicator_settings_list)

    # Hardstop to STOP all trading
    def add_hardstop(self):
        """
        This is a function that will look take a settings class and look for scenarios where we will perform a hardstop (and potentially restart)
        """
        pass


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
            name:str="", 
            klines:Database=None, 
            indicators:Database=None, 
            orderbook:Database=None, 
            signals:Database=None, 
            logic:Database=None, 
            positions:Database=None,
            trigger:bool=False, # Trigger to start building all databases
            retreive:bool=False, # If we want to get the settings
            verbose:bool=False
    ): 
        self.name = name
        self.verbose = verbose

        # TODO - Not sure if this should be changed at all - seems to complex to include in the class
        
        """
        Klines
        This will hold all the things that klines hold that comes from the kline + and the 
        indicators associated with it. We do have an indicator database that holds the 
        settings for the corresponding indicators.
        """
        self.klines = klines

        """
        Signals
        This will hold the boleans for example, if something is above another or if an 
        indicator has reached a certain level. These should be the things that specifically
        will signal that a trade should be put on. 
        """
        self.signals = signals

        """
        Indicator Settings
        Holds the settings for the indicators which will generally preside in the klines
        datbase. These include thinks like settings for EMAs and RSI etc.
        """
        self.indicators = indicators

        """
        Logic
        This involves any trading logic that needs to take place. For example if an EMA
        is above another EMA that would be under signal, there would also be a (very simple)
        piece of logic that would just open a trade. 
        """
        self.logic = logic

        """
        Orderbook - TODO
        Pretty self explanatory.
        """
        self.orderbook = orderbook

        """
        Positions - TODO
        """
        self.positions = positions

        # Check if any of the attr is None - Return Error
        for attr, value in self.__dict__.items():
            if isinstance(value, Database) and value is None:
                raise ValueError(f"The attribute {attr} of type Database is None.")
            
        if trigger:
            self.trigger()

    def __str__(self) -> str:
        return f"STRATEGY >> Name: {self.name} "
    
    """
    TODO - A more representative string that is able to define the whole database
    """
    def __str__(self) -> str:
        return f"STRATEGY: {self.name}"
    
    # TODO - create representation
    def __repr__(self) -> str:
        return f""

    def trigger(self):
        """
        This function 'triggers' all the required database to return their corresponding dataframes.
        In doing so, you can then start to either backtest or perform the strategy accordingly.
        """
        pass

    def add(self, indicator:Indicator):
        if self.verbose:
            print("ADDING")

    def save(self):
        if self.verbose:
            print("SAVING")
        
    