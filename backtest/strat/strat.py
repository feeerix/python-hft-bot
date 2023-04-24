# Imports
import pandas as pd
import pandas_ta as ta
import numpy as np

# Local Imports
from backtest.strat.indicator import indicator
from backtest.strat.settings.settings import import_setting, settings
from lib.file.writer import folder_exists, create_folder, file_exists, write_json
from lib.file.reader import get_json

class strategy:
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

    def init_df(self, df:pd.DataFrame):
        # Set up the dataframe
        self.df = df
        self.df['in_position'] = 0

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
            
    def write_settings(self):
        strat_folder = f'db/strategies/settings/'
        if not folder_exists(self.name, strat_folder):
            create_folder(self.name, strat_folder)
        
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

    def get_settings(self):
        strat_folder = f'db/strategies/settings/'

        self.indicator_settings_list = get_json(f"{strat_folder}{self.name}/indicator_settings.json")
        self.position_condition_settings = get_json(f"{strat_folder}{self.name}/position_settings.json")
        
        if self.verbose:
            print("Position Settings")
            print(self.position_condition_settings)
            print("Indicator Settings")
            print(self.indicator_settings_list)

    def add_hardstop(self):
        # Make sure the bot doesn't get you liquidated and lose all your money
        pass

    