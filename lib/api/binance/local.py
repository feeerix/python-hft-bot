import json

def filename(symbol:str, interval:str, year:str, month:str):
    return f"binance-{symbol}-{interval}-{year}-{month}.csv"