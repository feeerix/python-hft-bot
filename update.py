# Local Imports
from lib.api.updater import update
# from tests.battery import *
from lib.tools.interval import *
from lib.file.reader import *
from lib.tools.internal.crawler import Crawler

# Pair
pair_list = ['BTCUSDT', 'ETHUSDT', 'ETHBTC']

# Intervals
interval_list = ['4h']
# interval_list = ['1m', '5m', '15m', '1h', '4h']

update('Binance', pair_list, interval_list)