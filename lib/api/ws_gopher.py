# IMPORTS
import importlib
import websocket
import json
from abc import ABC, abstractmethod

# LOCAL IMPORTS
from lib.tools.exchange import Exchange, ExchangeType

"""
TODO - A prime candidate to be updated
so that I can start to run things live
Main challenge is to make sure I'm matching 
the data correctly.
"""
class ws_gopher(ABC):
    def __init__(self, exchange:ExchangeType, verbose:bool=False) -> None:
        self.exchange = exchange
        self.verbose = verbose

    def connect(self, ws_url:str):
        self.ws = websocket.create_connection(ws_url)
    
    def send(self, payload:dict):
        self.ws.send(
            json.dumps(
                payload  
            )
        )
    
    def close_connection(self):
        self.ws.close(
            1 # Arbitrary value
        )
        
    def receive(self):
        return self.ws.recv()
    
    @abstractmethod
    def ping(self):
        """
        Method to ping the corresponding websocket URL
        """
        pass
