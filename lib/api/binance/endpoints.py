# Import
import requests as req

# Local Import
from ..gopher import get_data

endpoints = {
    'ping': '/api/v3/ping',
    'server_time': '/api/v3/time',
    'server_status': '/sapi/v1/system/status',
    'exchange_info': '/api/v3/exchangeInfo',
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

def download_file(url, path, filename):
    r = req.get(f'{url}{filename}')
    f = open(f'{path}{filename}', 'wb')
    if r.status_code == 200:
        for chunk in r.iter_content(1024):
            f.write(chunk)
    f.close()