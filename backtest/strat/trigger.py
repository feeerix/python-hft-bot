# Imports
from enum import Enum
import pandas as pd
import pandas_ta as ta
from typing import List, Dict, Union

# Local Imports
from lib.file.writer import *
# from backtest.strat.settings import settings
from backtest.strat.settings.settings import Settings
from backtest.strat.composer import get_required_params
from lib.tools.interval import Interval


def above(values_a:List[Union[int, float]], values_b:List[Union[int, float]], inverse:bool=False) -> bool:
    if not inverse:
        return values_a[0] > values_b[0]
    else:
        return values_a[0] < values_b[0]
    
def below(values_a:List[Union[int, float]], values_b:List[Union[int, float]], inverse:bool=True) -> bool:
    return Trigger.above(values_a, values_b, inverse=inverse)

def cross(values_a:List[Union[int, float]], values_b:List[Union[int, float]], inverse:bool=False) -> bool:
    # Check for cross above condition
    if inverse:
        return values_a[-2] <= values_b[-2] and values_a[-1] > values_b[-1]
    
    # Check for cross below condition
    return values_a[-2] >= values_b[-2] and values_a[-1] < values_b[-1]


class TriggerFunction(Enum):
    ABOVE = "above"
    BELOW = "below"
    CROSS = "cross"

class Trigger:

    function_map = {
        TriggerFunction.ABOVE: above,
        TriggerFunction.BELOW: below,
        TriggerFunction.CROSS: cross
    }
    function_params = {
        TriggerFunction.CROSS: {"inverse": False},  # Default is "cross above"
        TriggerFunction.CROSS_BELOW: {"inverse": True}  # If you have a separate enum for "cross below"
        # ... add parameters for other functions if necessary
    }

    def __init__(self, _settings:Settings, _interval:Interval, verbose:bool=True, df:pd.DataFrame=None):
        # Verbosity
        self.verbose = verbose
        
        # Add the func into the class
        self.ind_func = getattr(ta, _settings.func_name)
        
        # Settings - a way to set up the indicator
        self.settings = _settings

        self.interval = _interval

        if df is not None:
            self.df = self.build_trigger(df)

    
    def __str__(self) -> str:
        return f"TRIGGER -- {self.settings.name}-{self.settings.columns}"

    @property
    def columns(self):
        return self.settings.columns
    
    def confirm(
            self, 
            rows:List[tuple], 
            function_type: TriggerFunction,
            column_mapping: List[str], # ["column_a", "column_b"]
            lookback:int=0
        ) -> bool:
        """
        This function will take in a list of rows, minimum of length 1, which is 
        always the length of the lookback.

        NOTE - row is a List of List, and is a essentially a 2D array

        """
        
        # _utility = ('above', 'above_value', 'below', 'below_value', 'cross')
        values_a = [row[column_mapping[0]] for row in rows[-(lookback+1):]]  # Using lookback to decide how many values you need
        values_b = [row[column_mapping[1]] for row in rows[-(lookback+1):]]

        # Get specific parameters for the function type from the function_params dictionary
        params = self.function_params.get(function_type, {})  # Default to an empty dictionary if no parameters are found

        # Now call the function using these values
        result = self.function_map[function_type](values_a, values_b, **params)

        # Handle the result as needed...
        return result


            # for row_idx in range(len(rows[interval])): # For each chronological row
                
            #     result = self.function_map[
            #         function_type
            #     ](

            #     )

                # print(row[interval_row_idx][chronological_row_idx])
                # result = self.function_map[function_type](values_a, values_b, **params)
    
    # def build_trigger(self, df:pd.DataFrame) -> pd.DataFrame:
    #     # initialise empty settings
    #     ind_settings = {}

    #     # Get the required parameters (OHLCV)
    #     req_params = get_required_params(self.settings.func_name)
    #     if self.verbose:
    #         print(f"ADDING: {self.settings.func_name}")

    #     # OHLCV

    #     for argument in req_params.keys():
            
    #         if req_params[argument]:
                
    #             if argument.startswith('series_'):
    #                 ind_settings.update({argument: df[self.settings.arguments[argument]]})
                
    #             elif (argument not in df.columns.to_list()) and type(self.settings.arguments[argument]) != str:
    #                 ind_settings.update({argument: self.settings.arguments[argument]})

    #             else: # OHLCV
    #                 ind_settings.update({argument: df[argument]})

    #         elif argument in self.settings.arguments.keys():
    #             ind_settings.update({argument: self.settings.arguments[argument]})
        
        
    #     ret_data = self.ind_func(**ind_settings)

    #     # --------------------------------------------------------------
    #     if type(ret_data) == pd.DataFrame:
    #         return pd.concat(df, ret_data, axis=1)
            
    #     elif type(ret_data) == pd.Series:
    #         self.settings.columns = [ret_data.name]
    #         return pd.concat([df, pd.DataFrame(ret_data, columns=self.settings.columns)], axis=1)

    #     else:
    #         print("SOMETHING WENT WRONG")
    #         print(type(ret_data))
    #         exit() # PANIC
        
    