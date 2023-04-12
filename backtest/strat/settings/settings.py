# Imports

# Local Imports
from lib.file.writer import *

class settings:
    # The main reason we create this class is so that we can load settings from the coresponding folders
    def __init__(self, name:str, func_name:str, settings:dict=None) -> None:
        # Add the setting details based on what's added

        # settings = {
        #     "name": setting_name
        #     "columns": [],
        #     "settings": {
        #         "arg1": default_value1,
        #         "arg2": default_value2
        #     }
        # }

        # Settings
        self.settings = {
            "name": name,
            "columns": [], # Programatically get column names
            "settings": settings
        }

    def validate_settings(self): 
        pass
        
         

    def write_settings(self):
        pass

    
    def get_settings(self):
        pass