# Import
import requests as req

endpoints = {
    'ping': '/api/v3/ping',
    'server_time': '/api/v3/time',
    'server_status': '/sapi/v1/system/status'
}

def ping() -> int:
    return req.get(f"https://data.binance.com{endpoints['ping']}")

def server_time() -> int:
    return req.get(f"https://data.binance.com{endpoints['server_time']}")

def server_status():
    return req.get(f"https://api.binance.com{endpoints['server_status']}")