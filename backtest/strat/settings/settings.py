# Imports

# Local Imports
from lib.file.writer import *
from backtest.strat.composer import get_required_params, write_required_params

class settings:
    # The main reason we create this class is so that we can load settings from the coresponding folders
    def __init__(self, name:str, func_name:str, arguments:dict=None, verbose:bool=True) -> None:
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
            "arguments": arguments
        }

        self.verbose = verbose
        if self.verbose:
            print(self.data)


    def validate_settings(self): 
        required_params = get_required_params(self.data['func_name'])
        ohlcv = ['open', 'high', 'low', 'close', 'volume']

        for data_type in required_params.keys():

            # Verbose print
            if self.verbose:
                print(f"{data_type} // {required_params[data_type]}")
            
            # If data is required and the data is NOT within settings
            if required_params[data_type] and data_type not in ohlcv:    
                if not data_type in self.data['arguments']:
                    # INVALID - return false
                    return False
        
        # Correct
        return True
         

    def write_settings(self):
        pass

    
    def get_settings(self):
        pass