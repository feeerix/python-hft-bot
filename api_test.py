# Imports
import pandas as pd
import pandas_ta as ta
import warnings
from datetime import datetime

# Loca Imports
# from lib.api.binance import

from lib.api.binance.binance import Binance
from db.database import Database
from lib.tools.symbol import Symbol
from lib.tools.interval import _Interval as Interval
from lib.tools.asset import Asset, AssetType
from lib.tools.network import Network
from backtest.strat.strategy import Strategy
from backtest.strat.indicator import Indicator
from backtest.strat.settings.settings import Settings

# from lib.tools.exchange import Exchange, ExchangeType
# from lib.file.reader import get_json

# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Ignoring future warning initially
warnings.simplefilter(action='ignore',category=FutureWarning)

start = 1569888000 # ETH / BTC
end = 1685592000

test_binance = Binance()
