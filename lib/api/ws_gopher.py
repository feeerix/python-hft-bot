# IMPORTS
import importlib
import websocket
import json

# LOCAL IMPORTS


class ws_gopher:
    def __init__(self, exchange:str, verbose:bool) -> None:
        self.exchange = exchange
        self.verbose = verbose

    def connect(self, ws_url:str):
        self.ws = websocket.create_connection(ws_url)
    
    def send(self, params:dict):
        self.ws.send(
            json.dumps(
                params  
            )
        )