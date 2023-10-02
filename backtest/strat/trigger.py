# Imports
from enum import Enum
import pandas as pd
import pandas_ta as ta
from typing import List, Dict, Union
import numpy as np

# Local Imports
from lib.file.writer import *
# from backtest.strat.settings import settings
from backtest.strat.settings.settings import Settings
from backtest.strat.composer import get_required_params
from lib.tools.interval import Interval


def above(
        row:List[tuple],
        series_a:str,
        series_b:str,
        inverse:bool=False, 
        **kwargs
    ) -> bool:
    """
    Row is length 1
    We get the values from getattr based on the series and compare them.
    """
    values_a = getattr(row[0], series_a)
    values_b = getattr(row[0], series_b)

    if not inverse:
        return values_a > values_b
    else:
        return values_a < values_b
    
def below(
        row:List[tuple],
        series_a:str,
        series_b:str,
        inverse:bool=True, 
        **kwargs
    ) -> bool:
    """
    Row is length 1
    We get the values from getattr based on the series and compare them.
    We just pass on everything onto the above function, but with inverse flag.
    """
    return above(row, series_a, series_b, inverse=inverse, **kwargs)

def above_value(
        row:List[tuple],
        series_a:str,
        series_b:str,
        inverse:bool=False, 
        **kwargs
    ) -> bool:
    """
    Row is of length 1.
    We get the values from getattr based on the series and compare them to a 
    specific value. We get the value from the kwargs.
    """
    values_a = getattr(row[0], series_a)
    if np.isnan(values_a) or np.isnan(kwargs['value']):    
        return False
    

    if not inverse:
        return values_a > kwargs['value']
    else:
        return values_a < kwargs['value']

def below_value(
        row:List[tuple],
        series_a:str,
        series_b:str,
        inverse:bool=True,
        **kwargs
    ):
    """
    Row is of length 1.
    We get the values from getattr based on the series and compare them to a 
    specific value. We get the value from the kwargs.

    We pass on the arguments with the inverse flag as true.
    """
    
    return above_value(row, series_a, series_b, inverse=inverse, **kwargs)

def cross(
        row:List[tuple],
        series_a:str,
        series_b:str,
        inverse:bool=False
    ) -> bool:
    """
    Row is of length 2.
    """
    values_a = [getattr(row[0], series_a), getattr(row[1], series_a)]
    values_b = [getattr(row[0], series_b), getattr(row[1], series_b)]
    

    # Check for cross above condition
    if inverse:
        return values_a[0] <= values_b[0] and values_a[1] > values_b[1]
    
    # Check for cross below condition
    return values_a[0] >= values_b[0] and values_a[1] < values_b[1]


class TriggerFunction(Enum):
    ABOVE = "above"
    BELOW = "below"
    CROSS_ABOVE = "cross_above"
    CROSS_BELOW = "cross_below"
    ABOVE_VALUE = "above_value"
    BELOW_VALUE = "below_value"

class Trigger:

    function_map = {
        TriggerFunction.ABOVE: above,
        TriggerFunction.BELOW: below,
        TriggerFunction.CROSS_ABOVE: cross,
        TriggerFunction.CROSS_BELOW: cross,
        TriggerFunction.ABOVE_VALUE: above_value,
        TriggerFunction.BELOW_VALUE: below_value
    }

    function_params = {
        TriggerFunction.CROSS_ABOVE: {"inverse": False, },  # Default is "cross above"
        TriggerFunction.CROSS_BELOW: {"inverse": True}  # If you have a separate enum for "cross below"
        # ... add parameters for other functions if necessary
    }

    function_lookback = {
        TriggerFunction.ABOVE: 1,
        TriggerFunction.BELOW: 1,
        TriggerFunction.CROSS_ABOVE: 2,
        TriggerFunction.CROSS_BELOW: 2,
        TriggerFunction.ABOVE_VALUE: 1,
        TriggerFunction.BELOW_VALUE: 1
    }

    def __init__(
            self, 
            _settings:Settings, 
            _interval:Interval, 
            verbose:bool=True, 
            df:pd.DataFrame=None,
            **kwargs
        ):
        # Verbosity
        self.verbose = verbose
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

    @property
    def lookback(self):
        return self.function_lookback[self.settings.func_name]
    
    def confirm(
            self, 
            rows:List[tuple], 
            function_type: TriggerFunction,
            arguments:dict
        ) -> bool:
        """
        This function will take in a list of rows, minimum of length 1, which is 
        always the length of the lookback.

        """
        # print("------------------------------------- CONFIRM FUNCTION IN TRIGGER -------------------------------------")
        # print(f"ROWS: {rows}")
        # print(f"FUNCTION_TYPE: {function_type}")
        # print(f"ARGUMENTS {arguments}")
        # print(getattr(rows[0], arguments['series_a']))
        
        arguments['row'] = rows
        arguments.update(self.function_params.get(function_type, {}))
        
        result = self.function_map[function_type](**arguments)
        
        return result

        # Now call the function using these values
        result = self.function_map[function_type](values_a, values_b, **params)
        # Handle the result as needed...
        return result

