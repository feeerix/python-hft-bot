# Imports
import pandas_ta as ta
import hashlib
from typing import Dict, Callable

# Local Imports
from lib.file.writer import *
from lib.tools.interval import Interval
# from backtest.strat.composer import get_required_params, write_required_params



def import_setting(settings_data:dict, verbose:bool=False):
    ret_data = Settings(
        settings_data["name"], 
        settings_data["func_name"],
        arguments=settings_data["arguments"],
        transform=settings_data["transform"],
        verbose=verbose
    )
    ret_data.data = settings_data
    return ret_data

"""
There are many things we want to change about our settings class

- We will want to make it less comlicated to initiate.
- Allow it to come up with it's own unique name, depending on the arguments
- All while still allowing it to interact with multiple classes as a "settings" class.

It might be more prudent to allow the class we want to adjust the setting for, to be input as an argument itself, so that we can return it modeified with our specific setting.
"""



class Settings:
    # The main reason we create this class is so that we can load settings from the coresponding folders
    def __init__(
            self, 
            name:str, 
            func_name:str, 
            arguments:dict=None, 
            transform:dict=None, 
            interval:Interval=None,
            verbose:bool=False, 
            **kwargs
        ) -> None:
        # Add the setting details based on what's added

        # settings = {
        #     "name": setting_name,
        #     "func_name": func_name 
        #     "arguments": {
        #         "arg1": default_value1,
        #         "arg2": default_value2
        #     }
        # }

        # Settings
        self.data = {
            "name": name,
            "func_name": func_name,
            "columns": [], # Programatically get column names
            "arguments": arguments,
            "transform": transform,
            # "open": arguments.pop('open_close')
        }

        _utility = ['above', 'above_value', 'below', 'below_value', 'cross']
        if self.data['func_name'] in _utility:
            self.utility = True
        else:
            self.utility = False

        self.verbose = verbose
        if self.verbose:
            print(self.data)
    
    def __str__(self) -> str:
        return self.data
    
    def hash(self) -> str:
        return hashlib.md5(bytes(repr(sorted(self.data.items())), "utf-8")).hexdigest()

    # TODO - Make sure is still required and works correct
    def validate_settings(self): 
        return True
         
