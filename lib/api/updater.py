# Local Imports
from lib.api.binance.binance import Binance

# from tests.battery import *
from lib.tools.interval import *

# Supported Exhchanges
supported_exchanges = ['Binance']

def update(exchange_name:str, symbols:list, intervals:list):
    exchange_init = globals()[exchange_name]
    exchange = exchange_init()
    for symbol in symbols:
        for interval in intervals:
            
            # TODO - update to make sure to check if we're doing millisecond timeframes or not in intervals
            exchange.update_klines(symbol, Interval.from_string(interval))


