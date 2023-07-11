# Imports
import pandas as pd
import pandas_ta as ta
import warnings

# Loca Imports
from db.db import database
from backtest.strat.strat import strategy
from backtest.strat.settings.settings import settings
from backtest.strat.indicator import indicator
from backtest.backtester import Backtester
from lib.cli.printer import *
from lib.cli.listener import *
from lib.file.reader import *

# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# -------------------
# Trying to do everything manually
# -------------------

exchange_info = get_json("./db/info/binance/exchange_info.json")

for symbol in exchange_info['symbols']:
    if symbol['status'] == "TRADING":
        if "USDT" in symbol['symbol']:
            print(symbol['symbol'])
exit()
