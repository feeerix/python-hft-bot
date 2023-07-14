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
# interval_list = ['4h']
interval_list = ['1m', '5m', '15m', '1h', '4h']

# if len(usdt_pairlist) > 50:
#     print("-- PAIRLIST --")
#     print(usdt_pairlist)
#     response = input("Do you want to proceed? All answers other than \"yes\" are considered no. ")
#     if response == "yes":
#         pass
#     else:
#         exit()

update('Binance', pair_list, interval_list)