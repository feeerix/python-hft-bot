# Imports
import pandas as pd
import pandas_ta as ta

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
    