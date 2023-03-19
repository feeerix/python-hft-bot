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
from lib.tools.interval import Interval

def process_kline(input_kline:list) -> dict:
    # Remember to remove unused 
    ret_data = pd.DataFrame(input_kline, columns=[
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
    # cols = ['open', 'high', 'low', 'close', 'volume', 'quote_volume', 'taker_buy_colume', 'taker_quote_volume']
    # for x in cols:
    #     ret_data[x].round(decimals=0)
    return ret_data


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
                
        
    def test_klines(self, symbol:str, interval:str, start:int=0, end:int=0, limit:int=500):
        
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
        

    def update_bulk_klines(self, symbol:str, interval:Interval, starttime:datetime=None):
        # Goes backward to get the last bulk till earliest

        # If we don't specify month
        if starttime is None:
            # get first of last month
            dt_starttime = datetime.today().replace(day=1,hour=0,second=0,microsecond=0) - relativedelta(months=1)
        else:
            # use specified start time (and works backwards!)
            dt_starttime = starttime
        
        pre_check(symbol.lower(), interval.str_rep())

        # Loop for each bulk file
        while True:
            # If file does not exist
            filepath = f"db/klines/{symbol.lower()}/{interval.str_rep()}/binance-{symbol}-{interval.str_rep()}-{dt_starttime.year}-{dt_starttime.month:02d}.csv"
            if not file_exists(filepath):
                # Download kline data
                bulk(
                    'klines',
                    self.verbose,
                    {
                        'symbol':symbol,
                        'interval': interval.str_rep().upper(),
                        'timestamp': dt_starttime.timestamp()
                    }
                )
            else:
                print(f'Already exists: {filepath}')
                break

            # Get the next time
            next_time = dt_starttime - relativedelta(months=1)
            
            # If the link exists
            if link_exists(
                # Getting url
                bulk_url(
                    'spot',
                    'klines',
                    symbol,
                    interval.str_rep(),
                    next_time.year,
                    f"{next_time.month:02d}"
                )
            ):
                # Link exists - Change the date
                dt_starttime -= relativedelta(months=1)
            else:
                # Link doesn't exist - exit loop
                break

    # Current function being created
    def update_klines(self, symbol:str, interval:Interval):
        
        # Last Close
        starttime = int(interval.last_close()/1000)
        
        # Limit
        limit = 1000

        # Start of the month
        finaltime = int(datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0).timestamp())
        filepath = f"db/klines/{symbol.lower()}/{interval.str_rep()}/binance-{symbol}-{interval.str_rep()}-{datetime.today().year}-{datetime.today().month:02d}.csv"
        
        # If this month's file exists
        if not file_exists(filepath):
            # Initialise empty df
            ret_data = pd.DataFrame(columns=[
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
            
            
        else:
            # Get existing df
            ret_data = pd.read_csv(filepath)

            # earliest time / final time
            finaltime = int((ret_data['time'].iloc[-1] / 1000) + interval.tc_rep())

            
        # Count how many we're going to download
        count = int(((starttime - finaltime) / interval.tc_rep()))

        if self.verbose:
            print(f"starttime: {starttime} // {datetime.fromtimestamp(starttime).isoformat()}")
            print(f"endtime: {finaltime} // {datetime.fromtimestamp(finaltime).isoformat()}")
            print(f"count: {count} // limit: {limit}")
            print("=="*32)
        
        temp_df = pd.DataFrame(columns=[
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
            
        # Get klines via fetch till start of the month - TODO
        while True:
            if self.verbose:
                print(f"Count reminaing: {count}")
            
            if count <= limit:
                limit = count
            
            starttime -= (interval.tc_rep() * limit) # tc * ms * limit

            last_df = process_kline(fetch_kline(
                self.base_url,
                self.verbose,
                {
                    'symbol': symbol,
                    'interval': interval.str_rep(),
                    'startTime': starttime * 1000,
                    'limit': limit
                }
            ).json())
            
            # append data
            temp_df = pd.concat([last_df, temp_df], ignore_index=True)

            # Get less limit
            count -= limit

            # Break once finished
            if count <= 0:
                break

        # Append temp to return data    
        ret_data = pd.concat([ret_data, temp_df], ignore_index=True)

        # Test print
        print(ret_data)
        print(f"First time: {datetime.fromtimestamp(int(ret_data['time'].iloc[0])/1000)}")
        print(f"Last time: {datetime.fromtimestamp(int(ret_data['time'].iloc[-1])/1000)}")
        
        # Write to file
        pd.DataFrame.to_csv(
            ret_data,
            filepath,
            index=False,
            float_format='%.0f'
        )

        # Then update klines via bulk
        self.update_bulk_klines(
            symbol,
            interval
        )
