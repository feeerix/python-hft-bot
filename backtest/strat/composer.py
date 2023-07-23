# Imports
import pandas_ta as ta
import inspect

# Local Imports
from lib.file.writer import *
from lib.file.reader import *

# from lib.tools.exchange import Exchange, ExchangeType
from lib.tools.internal.exchange_type import ExchangeType
from lib.tools.asset import Asset

# TODO - create way for us to compose a strategy
class Composer:
    """
    We shall use this as the class that creates the settings for strategies programatically

    Previously we had been using pandas_ta to create functions.
    """

    def __init__(self, verbose:bool=False):
        pass

    def add_setting(self):
        pass

    def write(self):
        pass

    def verify(self):
        pass


"""
Initial functions I was using?
"""

# Quick and dirty way to get the require params
def get_params(verbosity:bool=False):
    # Get functions
    ta_funcs = inspect.getmembers(ta, inspect.isfunction)
    ret_dat = {}

    # Iterate through each function
    for name, func in ta_funcs:
        if verbosity:
            print("--"*32)
            print(f"{name}")
            print("--"*32)
        
        ret_dat[name] = {}
        # A way to avoid a bug I was getting
        if not name.startswith('np'):

            # Get the names of all the parameters
            param_names = inspect.signature(func).parameters.keys()
            
            # Iterate through each parameter
            for param_name in param_names:
                if not param_name == "kwargs":
                    # Get the default value of the parameter
                    param_default = inspect.signature(func).parameters[param_name].default

                    if verbosity:
                        print(f"{name}.{param_name}")
                                    

                    # Check if the parameter is required
                    if param_default == inspect.Parameter.empty:
                        ret_dat[name][param_name] = True
                    else:
                        ret_dat[name][param_name] = False
    
    return ret_dat
    
def write_required_params(verbosity:bool=False): # TODO - Make sure to add verbosity and return
    write_data = get_params()

    # Write to file
    write_json(
        write_data,
        "required_ta_params.json",
        "db/strategies/indicators/"
    )

    # TODO - Make sure to add correct return values
    return True

"""
This is the only function that seems to appear in another file
"""
def get_required_params(func_name:str, verbosity:bool=False) -> dict:
    if verbosity:
        print(f"Getting required params for: {func_name}")

    return get_json("db/strategies/indicators/required_ta_params.json")[func_name]

def write_settings(setting_name:str, verbosity:bool=False): # TODO - Make sure to add verbosity and return

    # Get the parameters we want
    write_data = get_params()

    if verbosity is True:
        print(write_data)

    # Write to file
    write_json(
        write_data,
        f"{setting_name}.json",
        "db/strategies/indicators/settings/"
    )

    # TODO - Make sure to add correct return values
    return True

def get_settings(setting_name:str, verbosity:bool=False) -> dict:
    if verbosity:
        print(f"Getting required params for: {setting_name}")

    return get_json(f"db/strategies/indicators/settings/{setting_name}.json")