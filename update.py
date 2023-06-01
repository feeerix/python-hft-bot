

# Local Imports
from lib.api.updater import update
from tests.battery import *
from lib.tools.interval import *
from lib.file.reader import *

# Pair
pair_list = ['BTCUSDT', 'ETHUSDT', 'ETHBTC']
usdt_pairlist =[]

exchange_info = get_json("./db/info/binance/exchange_info.json")

for symbol in exchange_info['symbols']:
    if symbol['status'] == "TRADING":
        if "BUSD" in symbol['symbol']:
            usdt_pairlist.append(symbol['symbol'])

# Intervals
interval_list = ['4h']
# interval_list = ['5m']

update('Binance', usdt_pairlist, interval_list)