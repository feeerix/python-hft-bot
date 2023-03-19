# Local Imports
from lib.api.binance.interface import Binance
from tests.battery import *
from lib.tools.interval import *

# Initialise
binance = Binance()

# Pair
pair_list = ['BTCUSDT', 'ETHUSDT']

# Intervals
interval_list = ['1m', '15m', '1h', '4h']

# Update Loop
for pair in pair_list:
    for interval in interval_list:
        binance.update_klines(pair, Interval(interval,True))