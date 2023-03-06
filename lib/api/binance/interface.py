# Import
import json


# Local Import
from .endpoints import ping
from .endpoints import server_time as binance_time
from .endpoints import server_status
from lib.api.api import API

class Binance(API):
    def __init__(self) -> None:
        super().__init__("binance")

    def is_connected(self) -> bool: # function to check we get a ping response
        if ping().status_code == 200:
            return True # Connected!
        else:
            return False # Not Connected!
        
    def server_time(self) -> int: # function to check server time
        return binance_time().json()['serverTime']
    
    def server_status(self) -> bool: # function to check if server is under maintenence
        return server_status().json()