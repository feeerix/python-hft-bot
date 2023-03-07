# Import
import json


# Local Import
from .endpoints import ping, server_status, exchange_info
from .endpoints import server_time as binance_time

from lib.api.api import API

# Each exchange class is unique but is expected to follow some standards
class Binance(API):
    
    def __init__(self, verbosity:bool=True) -> None:
        # Initiates the API Class with name
        super().__init__("binance")
        self.verbose = verbosity

    # API Calls -> Server
    def is_connected(self) -> bool: # function to check we get a ping response
        if ping().status_code == 200:
            return True # Connected!
        else:
            return False # Not Connected!
        
    def server_time(self) -> int: # function to check server time
        return binance_time().json()['serverTime']
    
    def server_status(self) -> bool: # function to check if server is under maintenence
        return server_status().json()
    
    def exchange_info(self) -> bool:
        ret_data = exchange_info()

        # If we received an OK status
        if ret_data.status_code == 200:
            # Write file to JSON
            with open(f'db/info/{self.name}/exchange_info.json', "w") as outfile:
                outfile.write(json.dumps())
            
            # Return that we completed this task
            return True
        else:
            
            # Else something went wrong
            return False