# Imports
import pandas_ta as ta
import inspect

# Local Imports
from lib.file.writer import *
from lib.file.reader import *

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

def get_required_params(func_name:str, verbosity:bool=False):
    print(get_json("db/strategies/indicators/required_ta_params.json")[func_name])