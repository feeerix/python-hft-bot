# Imports
import pandas as pd
import pandas_ta as ta
import inspect

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
    

def check_func(ind_func:ta, settings:dict):
    print(ind_func.__code__.co_varnames)



class indicator:
    def __init__(self, ind_func:ta, settings:dict):
        # Add the func into the class
        self.ind_func = ind_func
        
        # Settings
        self.settings = settings
        # settings = {
        #     "columns": [],
        #     "settings": {
        #         "arg1": None,
        #         "arg2": None
        #     }
        # }
    
    def print_settings(self):
        print(self.settings)

    def add_indicator(self):
        pass
    
