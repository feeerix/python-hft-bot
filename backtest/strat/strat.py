# Imports
import pandas as pd
import pandas_ta as ta
import numpy as np

# Local Imports
from backtest.strat.indicator import indicator
from backtest.strat.settings import settings
from lib.file.writer import folder_exists, create_folder, file_exists, write_json
from lib.file.reader import get_json

class strategy:
    def __init__(self, name:str, verbose:bool=False, create:bool=False): 
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
        if create:
            self.get_settings()
        # ------------------

        self.longshort_condition_settings = {
            "long": [],
            "short": []
        }

    def init_df(self, df:pd.DataFrame):
        self.df = df
        self.df['in_position'] = 0

    def add_indicator(self, _indicator:indicator):
        self.indicator_settings_list.append(_indicator.settings.data)

        # Add individual indicator
        self.df = pd.concat(
            [
                self.df, # Existing DF
                _indicator.ret_indicator(self.df, self.verbose)], # New DF
            axis=1, 
            # ignore_index=True # -> removed index
        )

    
    def add_entry(self, _settings:settings):
        # Long/short entries

        if self.verbose:
            print(_settings.data)

        # 
        self.df[_settings.data['name']] = np.where((
                (self.df[_settings.data['arguments']['open'][1]].all(axis=1)) &
                (self.df[_settings.data['arguments']['open'][0]].sum(axis=1) == 0)
            ), 1, 0)
        
    def write_settings(self):
        strat_folder = f'db/strategies/settings/'
        if not folder_exists(self.name, strat_folder):
            create_folder(self.name, strat_folder)
        
        write_json(
            self.indicator_settings_list,
            f'{self.name}_settings.json',
            strat_folder+self.name+'/'
        )
    
    def get_settings(self):
        strat_folder = f'db/strategies/settings/'
        self.indicator_settings_list = get_json(f"{strat_folder}{self.name}/{self.name}_settings.json")


    def add_close(self, position_id: int):
        pass

    def add_hardstop(self):
        # Make sure the bot doesn't get you liquidated and lose all your money
        pass

    