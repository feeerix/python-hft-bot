

# Local Imports
from lib.api.updater import update
from tests.battery import *
from lib.tools.interval import *


# Pair
# pair_list = ['BTCUSDT', 'ETHUSDT']
pair_list = ['ETHUSDT']

# Intervals
# interval_list = ['1m', '5m', '15m', '1h', '4h']
interval_list = ['5m']

update('Binance', pair_list, interval_list)