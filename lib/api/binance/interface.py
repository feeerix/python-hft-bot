# Import
import json


# Local Import
from .endpoints import ping, server_status, exchange_info
from .endpoints import server_time as binance_time


from lib.api.api import API

# Each exchange class is unique but is expected to follow some standards
class Binance(API):
    
    def __init__(self, verbosity:bool=True) -> None:
        super().__init__("binance")
        self.verbose = verbosity

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
        with open('db/info/exchange_info.json', "w") as outfile:
            outfile.write(json.dumps(exchange_info().json()))
        return True