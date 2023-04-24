from lib.api.updater import update

# Local Imports
from tests.battery import *
from lib.tools.interval import *


# Pair
pair_list = ['BTCUSDT', 'ETHUSDT']

# Intervals
interval_list = ['1m', '15m', '1h', '4h']

update('Binance', pair_list, interval_list)