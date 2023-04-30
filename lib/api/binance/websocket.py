# IMPORTS
import websocket
import json
from datetime import datetime, timezone
import pandas as pd

# LOCAL IMPORTS
from ..ws_gopher import ws_gopher
from lib.api.binance.interface import process_kline
from lib.tools.interval import Interval
from lib.file.reader import get_json

ws_urls = [
    "wss://data-stream.binance.com:9443/ws",
    "wss://stream.binance.com:443/ws",
    "wss://stream.binance.com:9443/ws"
]

def parse_kline(kline:dict, verbose:bool = False) -> dict:
    # ret_kline = kline['k']
    # time,open,high,low,close,volume,close_time,quote_volume,trade_number,taker_buy_volume,taker_quote_volume,na
    kline_list = [
                kline['k']['t'], # time
                kline['k']['o'], # open
                kline['k']['h'], # high
                kline['k']['l'], # low
                kline['k']['c'], # close
                kline['k']['v'], # volume
                kline['k']['T'], # close_time
                kline['k']['q'], # quote_volume
                kline['k']['n'], # trade_number
                kline['k']['V'], # taker_buy_volume
                kline['k']['Q'], # taker_quote_volume
                kline['k']['B'], # na
    ]
    ret_data = process_kline(kline_list)

    # Test print
    if verbose:
        print(ret_data)

    return ret_data


def payload(method:str, stream_type:str, symbol:str, interval:str):
    param_list = []

    return {
        "method": method,
        "params": [

        ]
    }

class ws_agent(ws_gopher):
    def __init__(self, verbose:bool=False): 
        super().__init__('binance', verbose=verbose)
        self.last_ping = 0

    def create_connection(self, option:int):
        super().connect(ws_urls[option])
        self.last_ping = datetime.now(tz=timezone.utc)
    
    def subscribe(self, params:list, id:int):
        if self.verbose:
            for x in params:
                print(f"SUBSCRIBING TO: {x} // ID: {id}")
                
        super().send(
            {
                "method": "SUBSCRIBE",
                "params": params,
                "id": id
            }
        )
        
        response = json.loads(super().receive())
        
        if self.verbose:
            if response['result'] == None:
                print(f"SUBSCRIBE TO: {response['id']} -> Success!")

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

    def receive_data(self):
        response = json.loads(super().receive())

        print(response)
        print(type(response))
        return response

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