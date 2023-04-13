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
        self.settings = {
            "name": name,
            "func_name": func_name,
            "columns": [], # Programatically get column names
            "arguments": arguments
        }
        if verbose:
            print(self.settings)

    def validate_settings(self): 
        required_params = get_required_params(self.settings['func_name'])
        for data_type in required_params.keys():
            print(f"{data_type} // {required_params[data_type]}")
            # If data is required
            if required_params[data_type]:
                # and the data is NOT within settings
                if not data_type in self.settings['settings']:

                    # INVALID - return false
                    return False
        
        # Correct
        return True
         

    def write_settings(self):
        pass

    
    def get_settings(self):
        pass