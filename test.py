# Imports
import pandas as pd
import json
import pandas_ta as ta
import numpy as np

# Local Imports
from lib.api.binance.interface import Binance
from tests.battery import *
from lib.tools.interval import *


# Test
# filepath = f"db/klines/bnbusdt/1m/binance-BNBUSDT-1m-2023-03.csv"
# test = pd.read_csv(filepath)
# print(test)
# exit()
print(Binance().update_klines('BNBUSDT', Interval('1m',True)))
exit()
# binance = Binance()
# binance.update_bulk_klines('BTCUSDT','1m')
# binance.update_bulk_klines('BNBUSDT', '1m')
# print(binance.get_print_symbols())
Binance().update_klines(
    'LTCBTC',
    '1m'
)

exit()
with open("db/info/binance/exchange_info.json", "r") as exchange_info:
    test = json.load(exchange_info)


properties = [
    'symbol',
    'status',
    'baseAsset',
    'baseAssetPrecision',
    'quoteAsset',
    'quotePrecision',
    'quoteAssetPrecision'
]
asset_list = []
for asset in test['symbols']:
    current_asset = {}

    for prop in properties:
        current_asset[prop] = asset[prop]
    
    asset_list.append(current_asset)

for a in asset_list:
    print(a)
exit()
binance = Binance()

test_exact(
    True,
    Binance().is_connected,
    None,
    True
)

print(binance.server_status())