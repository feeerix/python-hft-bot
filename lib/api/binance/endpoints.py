# Import
import requests as req

# Local Import
from ..gopher import get_data

endpoints = {
    'ping': '/api/v3/ping',
    'server_time': '/api/v3/time',
    'server_status': '/sapi/v1/system/status',
    'exchange_info': '/api/v3/exchangeInfo'
}

def ping(base_url:str, verbose:bool) -> int:
    return req.get(f"{base_url}{endpoints['ping']}")

def server_time(base_url:str, verbose:bool) -> int:
    return req.get(f"{base_url}{endpoints['server_time']}")

def server_status(base_url:str, verbose:bool):
    return req.get(f"{base_url}{endpoints['server_status']}")

def exchange_info(base_url:str, verbose:bool):
    return req.get(f"{base_url}{endpoints['exchange_info']}")