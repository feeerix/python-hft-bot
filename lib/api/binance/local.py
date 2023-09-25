# Imports
import json

# Local Imports

def filename(exchange:str, symbol:str, interval:str, year:str, month:str):
    return f"{exchange}-{symbol}-{interval}-{year}-{month}.csv"