# Import
import json
import pandas as pd

# Local Import
from .endpoints import ping, server_status, exchange_info, fetch_kline
from .endpoints import server_time as binance_time
from lib.file.writer import *

from lib.api.api import API


def process_kline(input_kline:list) -> dict:
    # Remember to remove unused 
    return pd.DataFrame(input_kline, columns=[
        'time',
        'open',
        'high',
        'low',
        'close',
        'volume',
        'close_time',
        'quote_volume',
        'trade_number',
        'taker_buy_volume',
        'taker_quote_volume',
        'na'
    ])

def pre_check(exchange:str, symbol:str, interval:str):
    # Check that the folder has been created
    if not folder_exists(symbol, f"db/klines/"):
        create_folder(
            symbol,
            "db/klines/"
        )
    
    if not folder_exists(interval, f"db/klines/{symbol}/"):
        create_folder(
            interval,
            f"db/klines/{symbol}/"
        )

def write_db(input_db:pd.DataFrame, exchange:str, symbol:str, interval:str, date:str):
    # Check that the folder has been created
    if not folder_exists(symbol, f"db/klines/"):
        create_folder(
            symbol,
            "db/klines/"
        )
    
    if not folder_exists(interval, f"db/klines/{symbol}/"):
        create_folder(
            interval,
            f"db/klines/{symbol}/"
        )
    
    input_db.to_csv(
        f"db/klines/{symbol}/{interval}/{exchange}-{symbol}-{interval}-{date}.csv",
        index=False
    )

# Each exchange class is unique but is expected to follow some standards
class Binance(API):
    
    def __init__(self, url_index:int=0, verbosity:bool=True) -> None:
        # Initiates the API Class with name
        super().__init__("binance")

        # Verbose
        self.verbose = verbosity

        # Get base URL
        self.base_url = super().base_url(url_index)    

    # API Calls -> Server
    def is_online(self) -> bool: # function to check we get a ping response
        if ping(self.base_url, self.verbose).status_code == 200:
            return True # Connected!
        else:
            return False # Not Connected!
        
    def server_time(self) -> int: # function to check server time
        return binance_time(self.base_url, self.verbose).json()['serverTime']
    
    def server_status(self) -> bool: # function to check if server is under maintenence
        return server_status(self.base_url, self.verbose).json()
    
    def exchange_info(self) -> bool:
        ret_data = exchange_info(self.base_url, self.verbose)

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
        
    def test_klines(self, symbol:str="", interval:str="", start:int=0, end:int=0, limit:int=500):
        
        ret_data = process_kline(fetch_kline(
            self.base_url,
            self.verbose,
            {
                'symbol': 'ETHBTC',
                'interval': '1m',
                'limit': 500
            }
        ).json())
        # print(ret_data.status_code)
        print(ret_data)
        write_db(ret_data, self.name, symbol, interval, '2023-03')

    def test_bulk_klines(self):
        