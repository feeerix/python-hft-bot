# Import
import requests as req

endpoints = {
    'ping': '/api/v3/ping'
}

def ping() -> bool:
    ret_data = req.get(f"https://data.binance.com{endpoints['ping']}")
    print(ret_data.status_code)
    print(ret_data.json())