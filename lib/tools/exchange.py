# IMPORTS
from enum import Enum
from abc import ABC, abstractmethod
import json

# lOCAL IMPORT
from lib.file.reader import get_json, get_list


class ExchangeType(Enum):
    BINANCE = "binance"
    BYBIT = "bybit"
    PHEMEX = "phemex"

class Exchange(ABC):
    
    def __init__(self, exchange:ExchangeType):
        # Set exchange type
        self.exchange_type = exchange
        
        # Filepath
        self.filepath = f"lib/api/{self.exchange_type.name.lower()}/"
        self.base_url_list = get_list(self.filepath+'base_urls.json')
        
    def __repr__(self) -> str:
        return self.exchange_type

    def __str__(self) -> str:
        return self.exchange_type.name
    
    def get_info(self) -> dict:
        return get_json(f"db/info/{self.exchange_type.name.lower()}/exchange_info.json")
    
    """
    Currently experimenting with abstract method
    """
    @abstractmethod
    def is_online(self) -> bool:
        """
        Normally used to check that the exchange is still online.
        It might be a good idea to also make sure we can check with multiple different base URLs

        Returns a boolean to say that it is online.
        """
        pass


    @abstractmethod
    def server_time(self) -> int: # function to check server time
        """
        Server time - returns int that is the current timestamp for the server
        TODO - still deciding what specific timestamp format (seconds or ms etc)
        """
        pass
    
    @abstractmethod
    def server_status(self) -> bool: # function to check if server is under maintenence
        """
        Server Status
        """
        pass
    
    @abstractmethod
    def exchange_info(self) -> bool:
        """
        Exchange Info

        Always writes to: db/info/{exchange}/exchange_info.json
        """
        pass