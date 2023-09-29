# Imports
import pandas as pd
import pandas_ta as ta
from typing import List

# Local Imports
from lib.file.writer import *
from backtest.strat.settings.settings import Settings
from backtest.strat.composer import get_required_params
from lib.tools.interval import Interval
from backtest.position import Position, PositionType, Trade, TradeArgs



class Intents:
    type_mapping = {
        PositionType.LONG: "placeholder",
        PositionType.SHORT: "placeholder",
        PositionType.OPTION: "placeholder",
        PositionType.ARB: "placeholder"
    }

    def __init__(self, _settings:Settings, _interval:List[Interval], verbose:bool=True, df:pd.DataFrame=None):
        # Verbosity
        self.verbose = verbose
        
        # Add the func into the class
        self.ind_func = getattr(self, self.type_mapping[PositionType.from_string(_settings.func_name.upper())])
        
        # Settings - a way to set up the indicator
        self.settings = _settings

        """
        Relates to the interval we want to reference.
        If there is a signal that requires multiple intervals we will do this in logic
        as we look at this from a database perspective?
        """
        self.interval = _interval

        if df is not None:
            self.df = self.build_signal(df)

    
    def __str__(self) -> str:
        return f"LOGIC -- {self.settings.name}-{self.settings.arguments}"

    @property
    def columns(self):
        return self.settings.columns
    
    @property
    def plumbing(self):
        """
        Defines how the logic works and will be derived based on the settings.
        It can then be checked if logic is true, and then be executed.
        """
        pass

    def execute(self):
        """
        Executes whatever logic is required - creating a position for example etc
        """
        pass

    def check(
            self, 
            row:tuple # Part of the data we're taking in

        ) -> bool:
        """
        This is returns a boolean if the specific logic has been met.
        """

        is_valid = True
        for col in self.settings.columns[True]:
            if getattr(row, col) == 0:
                is_valid = False
                break
        for col in self.settings.columns[False]:
            if getattr(row, col) == 1:
                is_valid = False
                break

        return is_valid
    
    def placeholder(self):
        print("test")