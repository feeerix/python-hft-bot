# Imports
import pandas as pd
import pandas_ta as ta
from typing import List
from enum import Enum

# Local Imports
from lib.file.writer import *
from backtest.strat.settings.settings import Settings
from backtest.strat.composer import get_required_params
from lib.tools.interval import Interval
from backtest.position import Position, PositionType, Trade, TradeArgs
from backtest.strat.trigger import Trigger, TriggerFunction

class Intents:
    """
    An intent is a class with that holds information about creating a position.
    
    """

    type_mapping = {
        PositionType.LONG: "placeholder",
        PositionType.SHORT: "placeholder",
        PositionType.OPTION: "placeholder",
        PositionType.ARB: "placeholder"
    }

    def __init__(
            self, 
            _settings:Settings, 
            _interval:List[Interval], 
            verbose:bool=True, 
            df:pd.DataFrame=None
        ):
        
        # Verbosity
        self.verbose = verbose
        # Settings - a way to set up the indicator
        self.settings = _settings
        # Position - Initialises empty position
        self.position = Position(self.settings.func_name)
        # Active
        self.active = True

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

    def conditions(
            self
        ):
        """
        This function will check if the entry/exit conditions have been met. This can 
        define whether someone can enter based on risk, whether a position is open etc.
        
        """
        if self.active:
            pass
        else:
            return False

    def check(
            self,
            df:pd.DataFrame, # We just pass in the whole DF
            current_idx:int,
        ) -> bool:
        """
        This is returns a boolean if the specific logic has been met.
        There is a "True" and a "False" key value pair and they both have to be
        met with all their Triggers being true or false to open the position.
        """

        is_valid = True
        
        for col in self.settings.columns[True]:
            row_chunk = list(df[current_idx:current_idx+col.lookback].itertuples(index=False))    
            if not col.confirm(
                row_chunk, # rows:List[tuple], 
                col.settings.func_name, # function_type: TriggerFunction
                col.settings.arguments, # column_mapping: List[str], # ["column_a", "column_b"] - THIS LINE HERE
                # values=col.settings.arguments['value']
            ):
                is_valid = False
                break

        return is_valid
    
    def placeholder(self):
        print("placeholder test print")
        exit()