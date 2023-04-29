# IMPORTS
import websocket
import json
from datetime import datetime, timezone

# LOCAL IMPORTS
from ..ws_gopher import ws_gopher
from lib.tools.interval import Interval

ws_urls = [
    "wss://data-stream.binance.com:9443/ws",
    "wss://stream.binance.com:443/ws",
    "wss://stream.binance.com:9443/ws"
]

def parse_kline(kline:dict) -> dict:
    pass
    # return kline[]



def payload(method:str, stream_type:str, symbol:str, interval:str):
    
    return {
        "method": method,
        "params": []
    }

class ws_agent(ws_gopher):
    def __init__(self): 
        super().__init__('binance')
        self.last_ping = 0

    def connect(self, option:int):
        super().connect(ws_urls[option])
        self.last_ping = datetime.now(tz=timezone.utc)
    
    def subscribe(self, params:list, id:int):
        super().send(
            {
                "method": "SUBSCRIBE",
                "params": params,
                "id": id
            }
        )

    def unsubscribe(self, params:list, id:int):
        super().send(
            {
                "method": "UNSUBSCRIBE",
                "params": params,
                "id": id
            }
        )
    
    def ping(self):
        super().ws.ping()

    def parse(self):
        response = super().receive()


    def send(self, method:str, params:list):
        self.ws.send(
            json.dumps(
                {
                    "method": method,
                    "params": params,
                    "id": 1
                }
            )
        )

    def connect(self):
        pass
        # ws = websocket.create_connection(ws_url)
        
        # ws.send(
        #     json.dumps(
        #         {
        #         "method": "SUBSCRIBE",
        #         "params":
        #         [
        #             "ethusdt@kline_1m"
        #         ],
        #         "id": 1
        #         }
        #     )
        # )
        # counter = 0
        # while True:
        #     response = ws.recv()
        #     print(f"RESPONSE: {response}")
        #     counter += 1
        #     if counter > 5:
        #         ws.close(1)
        #         break