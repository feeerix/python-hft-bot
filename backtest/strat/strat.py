# Imports
import pandas as pd
import pandas_ta as ta
import numpy as np
from hashlib import sha256
import time

# Local Imports
from backtest.strat.indicator import indicator
from backtest.strat.settings.settings import import_setting, settings
from lib.file.writer import folder_exists, create_folder, file_exists, write_json
from lib.file.reader import get_json

class strategy:
    def __init__(self, name:str, df:pd.DataFrame, verbose:bool=False, retreive:bool=False, higher_df:list=None): 
        self.name = name
        self.verbose = verbose
        self.df = None
        self.h_df = higher_df

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
                self.add_indicator(indicator(new_setting), recording=False)

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
    def add_indicator(self, _indicator:indicator, recording:bool=True):
        if self.verbose:
            print(_indicator.settings.data)

        # If we want to write the settings
        if recording:
            self.indicator_settings_list.append(_indicator.settings.data)

        # Add individual indicator
        self.df = pd.concat(
            [
                self.df, # Existing DF
                _indicator.ret_indicator(self.df, self.verbose)
            ], # New DF
            axis=1, 
            # ignore_index=True # -> removed index
        )

        # for tf in self.h_df:
        #     tf = pd.concat(
        #         [
        #             self.df, # Existing DF
        #             _indicator.ret_indicator(tf, self.verbose)
        #         ], # New DF
        #         axis=1, 
        #         # ignore_index=True # -> removed index
        #     )

    # Add entry conditions
    def add_entry(self, _settings:settings, recording:bool=True):
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
    def add_close(self, _settings:settings, recording:bool=True):    
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

    