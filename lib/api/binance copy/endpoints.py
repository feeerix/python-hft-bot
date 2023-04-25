# Import
import requests as req
from datetime import datetime
import pandas as pd
import os

# Local Import
from ..gopher import get_data

from lib.file.finder import *

endpoints = {
    'ping': '/api/v3/ping',
    'server_time': '/api/v3/time',
    'server_status': '/sapi/v1/system/status',
    'exchange_info': '/api/v3/exchangeInfo', # spot
    'klines': '/api/v3/klines'
}

def ping(base_url:str, verbose:bool) -> int:
    if verbose:
        print("ping!")
    return get_data(base_url, endpoints['ping'], verbose)

def server_time(base_url:str, verbose:bool) -> int:
    return get_data(base_url, endpoints['server_time'], verbose)

def server_status(base_url:str, verbose:bool):
    return get_data(base_url, endpoints['server_status'], verbose)

def exchange_info(base_url:str, verbose:bool):
    return get_data(base_url, endpoints['exchange_info'], verbose)

def fetch_kline(base_url:str, verbose:bool, params:dict):
    if verbose:
        print(f"Params: {params}")
        
    return req.get(
        f"{base_url}{endpoints['klines']}",
        params=params
    )

def bulk_url(trade_type:str, data_type:str, symbol:str, interval:str, year:str, month:str):
    return f"https://data.binance.vision/data/{trade_type}/monthly/{data_type}/{symbol}/{interval}/{symbol}-{interval}-{year}-{month}.zip"

def bulk(base_url:str, verbose:bool, params:dict):
    if verbose:
        print(f"Params: {params}")
    
    # Get the month and year
    year = datetime.fromtimestamp(params['timestamp']).strftime("%Y")
    month = datetime.fromtimestamp(params['timestamp']).strftime("%m")
    
    # Create the URL
    current_url = bulk_url(
            "spot",
            "klines",
            params['symbol'].upper(),
            params['interval'],
            year,
            month
        )

    # Filename and filepath
    filename = f'binance-{params["symbol"]}-{params["interval"]}-{year}-{month}'
    filepath = f'db/klines/{params["symbol"]}/{params["interval"]}/'
    
    # Download file
    download_file(
        current_url,
        filepath,
        filename+".zip"
    )
    # unzip the file
    unzip_file(
        filepath,
        filename
    )
    og_filename = f"{params['symbol'].upper()}-{params['interval']}-{year}-{month}.csv"

    # read csv as pandas dataframe
    data = pd.read_csv(
        filepath+og_filename,
        header=None,
        names=[
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
        ]
    )

    # Write to csv
    data.to_csv(
        filepath+filename+".csv",
        index=False
    )

    # Test print
    if verbose:
        print(data)
    
    # remove files
    os.remove(filepath+og_filename)
    os.remove(filepath+filename+".zip")

    