# Import
import json
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Local Import
from .endpoints import ping, server_status, exchange_info, fetch_kline, bulk, bulk_url
from .endpoints import server_time as binance_time
from lib.file.writer import *
from lib.file.reader import file_exists

from lib.api.api import API
from lib.file.finder import *

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

def pre_check(symbol:str, interval:str):
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
                json.dump(ret_data.json(), outfile)
            
            # Return that we completed this task
            return True
        else:
            
            # Else something went wrong
            return False
        
    def get_print_symbols(self, live:bool=False, status:str="TRADING") -> list:
        sym_list = []
        if live:
            # Make sure we have the latest info
            self.exchange_info() # Download the latest info and if done correctly
        
        # Open the file
        with open(f'db/info/{self.name}/exchange_info.json', "r") as f:
            
            # Pull the data
            data = json.load(f)

        # For each line in the data['symbols']
        for sym in data['symbols']:
            # If the status is what we're looking for (generally trading)
            if sym['status'] == status:

                # Add the symbol to the list
                sym_list.append(sym['symbol'])
        
        return sym_list
                
        
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

        print(ret_data)
        write_db(ret_data, self.name, symbol, interval, '2023-03')

    def test_bulk_klines(self, symbol:str, interval:str, starttime:datetime=None):
        # Goes backward to get the last bulk till earliest

        # If we don't specify month
        if starttime is None:
            # get first of last month
            dt_starttime = datetime.today().replace(day=1,hour=0,second=0,microsecond=0) - relativedelta(months=1)
        else:
            # use specified start time (and works backwards!)
            dt_starttime = starttime
        
        pre_check(symbol.lower(), interval)

        # Loop for each bulk file
        while True:
            # If file does not exist
            filepath = f"db/klines/{symbol.lower()}/{interval}/binance-{symbol}-{interval}-{dt_starttime.year}-{dt_starttime.month:02d}.csv"
            if not file_exists(filepath):
                # Download kline data
                bulk(
                    'klines',
                    self.verbose,
                    {
                        'symbol':symbol,
                        'interval': interval,
                        'timestamp': dt_starttime.timestamp()
                    }
                )
            else:
                print(f'Already exists: {filepath}')

            # Get the next time
            next_time = dt_starttime - relativedelta(months=1)
            
            # If the link exists
            if link_exists(
                # Getting url
                bulk_url(
                    'spot',
                    'klines',
                    symbol,
                    interval,
                    next_time.year,
                    f"{next_time.month:02d}"
                )
            ):
                # Link exists - Change the date
                dt_starttime -= relativedelta(months=1)
            else:
                # Link doesn't exist - exit loop
                break
