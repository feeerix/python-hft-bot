# Imports
import pandas as pd
import pandas_ta as ta
import warnings
from datetime import datetime

# Loca Imports
# from db.database import Database
# from backtest.strat.strategy import Strategy
# from backtest.strat.settings.settings import Settings
# from backtest.strat.indicator import Indicator
# from backtest.backtester import Backtester
# from lib.cli.printer import *
# from lib.cli.listener import *
# from lib.file.reader import *

from backtest.strat.composer import get_required_params, write_required_params

# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# -------------------
# Trying to do everything manually
# -------------------


# get_required_params()
write_required_params()

exit()
exchange_info = get_json("./db/info/binance/exchange_info.json")

for symbol in exchange_info['symbols']:
    if symbol['status'] == "TRADING":
        if "USDT" in symbol['symbol']:
            print(symbol['symbol'])
exit()
