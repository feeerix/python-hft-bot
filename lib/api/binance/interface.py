# Import
import json
import pandas as pd

# Local Import
from .endpoints import server_time as binance_time, endpoint_functions
from lib.file.writer import *
from lib.file.finder import *

"""
This function processes the kline.

I can instantly see that it might be agood idea to make sure to update this so it remains performant.
"""

def process_kline(input_kline:list) -> pd.DataFrame:

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