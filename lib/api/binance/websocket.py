# IMPORTS
import websocket
import json
from datetime import datetime, timezone
import pandas as pd

# LOCAL IMPORTS
from ..ws_gopher import ws_gopher
from lib.api.binance.interface import process_kline
from lib.cli.printer import line
from lib.tools.interval import Interval
from lib.file.reader import get_json

ws_urls = [
    "wss://data-stream.binance.com:9443/ws",
    "wss://stream.binance.com:443/ws",
    "wss://stream.binance.com:9443/ws"
]


"""
STREAM ID GOES LIKE THIS:

SYMBOL - 2 DIGITS
TYPE - 1 DIGIT
INTERVAL - 1 DIGIT // LEVEL - 1 DIGIT

"""


def parse_stream_id(id_config:dict, stream_id:str) -> dict:
    pass

def return_stream_id(id_config:dict, **kwargs) -> int:
    if kwargs['stream_type'] == 'kline':
        return int(
            str(id_config['symbol'][kwargs['symbol']]) +
            str(id_config['stream_type'][kwargs['stream_type']]) +
            str(id_config['interval'][kwargs['interval']])
        )
    elif kwargs['stream_type'] == 'depth':
        return int(
            str(id_config['symbol'][kwargs['symbol']]) +
            str(id_config['stream_type'][kwargs['stream_type']]) +
            str(id_config['level'][kwargs['level']])
        )

def parse_kline(kline:dict, verbose:bool = False) -> dict:
    
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
    
    # Return data and process into dataframe
    ret_data = process_kline([kline_list])

    # Test print
    if verbose:
        print(ret_data)

    return ret_data

# Dirty way to get the stream name
def stream_type(stream_type:str, symbol:str="", interval:str="", level:str=""):
    if stream_type == 'kline':
        return f'{symbol}@kline_{interval}'
    elif stream_type == 'depth':
        if level == "0":
            return f'{symbol}@depth@100ms'
        else:
            return f'{symbol}@depth{level}@100ms'
    else:
        return f'{symbol}@{stream_type}'

# Dirty way to get payload
def payload(method:str, stream_type:str, symbol:str="", interval:str="", level:int=0, **kwargs):
    # TODO - integrate update-time to both of the above functions
    return {
        "method": method,
        "params": [
            stream_type(stream_type, symbol, interval, level)
        ]
    }

class ws_agent(ws_gopher):
    def __init__(self, verbose:bool=False): 
        super().__init__('binance', verbose=verbose)
        self.last_ping = 0
        self.ws_table = get_json('lib/api/binance/config/websocket_table.json')

    def create_connection(self, option:int):
        # create connection
        super().connect(ws_urls[option])

        # Make sure to ping immediately
        self.ping()

        # Test print
        if self.verbose:
            print(f"LAST PING: {self.last_ping}")
    
    def subscribe(self, params:dict):

        stream_name = stream_type(**params)
        id = return_stream_id(self.ws_table, **params)
        
        # Test print
        if self.verbose:
            print(line)
            print(f"SUBSCRIBING TO: {stream_name} // ID: {id}")
        
        super().send(
            {
                "method": "SUBSCRIBE",
                "params": [stream_name],
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
        if self.verbose:
            print("Sending Ping!")

        self.ws.ping()

        # update the last ping
        self.last_ping = int(datetime.now(tz=timezone.utc).timestamp())

    def receive_data(self):
        # Compute response
        response = json.loads(super().receive())
        ret_data = None

        if 'result'in response.keys():
                if self.verbose:
                    if response['result'] == None:
                        print(f"RESPONSE > {response['id']} -> SUCCESS")
                    else:
                        print(f"RESPONSE > {response['id']} -> UNSUCCESSFUL")
                return response
        
        # Dirty way to get partial depth
        elif 'e' not in response.keys():
            # Test print
            if self.verbose:
                print("-- RESPONSE -- ")
                print(response)
            
            # TODO - potentially need to update this part
            return {
                'e': 'depth',
                'data': response 
            }

        # if kline
        elif response['e'] == 'kline':
            # parse kline
            ret_data = parse_kline(response)

            # test print
            if self.verbose:
                print(f"{line}")
                print(f"PARSED: {response} -> {type(ret_data)}")
        
        elif response['e'] == 'depthUpdate':
            if self.verbose:
                print("Depth Update")
                print(f"{response}")
            
            return response
        
        if (int(datetime.now(tz=timezone.utc).timestamp()) - self.last_ping) > 170:
            self.ping()
        
        return ret_data