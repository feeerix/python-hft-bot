# Imports
import pandas as pd
import pandas_ta as ta
import warnings
from datetime import datetime

# Loca Imports
# from lib.api.binance.binance import Binance
from db.database import Database, DatabaseType
from lib.tools.symbol import Symbol
from lib.tools.exchange import ExchangeType
from lib.tools.interval import Interval
from lib.tools.asset import Asset, AssetType
from lib.tools.network import Network
from backtest.strat.strategy import Strategy
from backtest.strat.indicator import Indicator
from backtest.strat.settings.settings import Settings

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)

pd.set_option('display.float_format', lambda x: '%.5f' % x)

start = 1569888000
end = 1685592000

"""
First we are looking to update the way we handle dataframes.
Let's also try to clean everything up and make everything more performant.

"""


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

# test_binance = Binance()

# Database().kline_df('ETHUSDT',"4h",start,end)
eth = Asset("Ethereum", "ETH", "0x0", AssetType.COIN, Network.ETHEREUM)
usdt = Asset("Tether", "USDT", "0x0", AssetType.TOKEN, Network.ETHEREUM)

ethusdt = Symbol("ETHUSDT", [eth, usdt])
interval1 = str(Interval._4h)

# def _kline_df(self, symbol:Symbol, interval:Interval, starttime:int, endtime:int) -> pd.DataFrame:

klines_4h = Database("ethusdt_klines", DatabaseType.KLINES, True, symbol=ethusdt, interval=Interval._4h, starttime=start, endtime=end, source=ExchangeType.BINANCE)
klines_1h = Database("ethusdt_klines", DatabaseType.KLINES, True, symbol=ethusdt, interval=Interval._1h, starttime=start, endtime=end, source=ExchangeType.BINANCE)
klines_15m = Database("ethusdt_klines", DatabaseType.KLINES, True, symbol=ethusdt, interval=Interval._15m, starttime=start, endtime=end, source=ExchangeType.BINANCE)
klines_5m = Database("ethusdt_klines", DatabaseType.KLINES, True, symbol=ethusdt, interval=Interval._5m, starttime=start, endtime=end, source=ExchangeType.BINANCE)
klines_1m = Database("ethusdt_klines", DatabaseType.KLINES, True, symbol=ethusdt, interval=Interval._1m, starttime=start, endtime=end, source=ExchangeType.BINANCE)

indicator_list = [
    Indicator(Settings("ema8", "ema", {'length': 8})),
    Indicator(Settings("ema21", "ema", {'length': 21})),
    Indicator(Settings("ema144", "ema", {'length': 144})),
    Indicator(Settings("ema233", "ema", {'length': 233})),
    Indicator(Settings("stochrsi", "stochrsi", {"length": 21, "rsi_length": 21, "k": 5, "d": 5})),
    Indicator(Settings("atr", "atr", {"length": 21, "mamode": "ema"}))
]

indicators_4h = Database(
    "", # Name
    DatabaseType.INDICATORS, # To list that this is a database of indicators
    True, # Verbosity
    symbol=ethusdt, # Symbol indicators relate to
    interval=Interval._4h, # Interval it relates to
    indicators=indicator_list, # The list of indicators to be added
    recording=False # If I'm recording and saving the data,
    )

indicators_1h = Database(
    "", # Name
    DatabaseType.INDICATORS, # To list that this is a database of indicators
    True, # Verbosity
    symbol=ethusdt, # Symbol indicators relate to
    interval=Interval._1h, # Interval it relates to
    indicators=indicator_list, # The list of indicators to be added
    recording=False # If I'm recording and saving the data,
    )

indicators_15m = Database(
    "", # Name
    DatabaseType.INDICATORS, # To list that this is a database of indicators
    True, # Verbosity
    symbol=ethusdt, # Symbol indicators relate to
    interval=Interval._15m, # Interval it relates to
    indicators=indicator_list, # The list of indicators to be added
    recording=False # If I'm recording and saving the data,
    )

indicators_5m = Database(
    "", # Name
    DatabaseType.INDICATORS, # To list that this is a database of indicators
    True, # Verbosity
    symbol=ethusdt, # Symbol indicators relate to
    interval=Interval._5m, # Interval it relates to
    indicators=indicator_list, # The list of indicators to be added
    recording=False # If I'm recording and saving the data,
    )

indicators_1m = Database(
    "", # Name
    DatabaseType.INDICATORS, # To list that this is a database of indicators
    True, # Verbosity
    symbol=ethusdt, # Symbol indicators relate to
    interval=Interval._1m, # Interval it relates to
    indicators=indicator_list, # The list of indicators to be added
    recording=False # If I'm recording and saving the data,
    )

"""
You can see that the specific klines and indicators are all related to a symbol and interval.
We build all the dataframes separately and add the indicators accordingly.

When we want to add the signals (which might rely on multiple timeframes and symbols), we then
add those after we've built all the kline and indicator dataframes.
"""

klines_dbs = [
    klines_4h, 
    # klines_1h, 
    # klines_15m, 
    # klines_5m, 
    # klines_1m
]

indicator_dbs = [
    indicators_4h,
    # indicators_1h,
    # indicators_15m,
    # indicators_5m,
    # indicators_1m
]


test_strat = Strategy(
    name="test1", 
    klines=klines_dbs,
    indicators=indicator_dbs,
    orderbook=[Database(db_type=DatabaseType.ORDERBOOK)], # TODO - need to update exchange class to add ws functions
    signals=Database(db_type=DatabaseType.SIGNALS),
    logic=Database(db_type=DatabaseType.LOGIC),
    positions=Database(db_type=DatabaseType.POSITIONS),
    verbose=True,
)

print("CREATED TEST STRAT")
test_strat.build()

print(test_strat.klines[0].df)

# for x in test_strat.klines:
#     print(x.df)

exit()

"""
Now that we have created both dataframes as well as added the indicators, let's see if we want to perform the modelling within the strategy class?
"""

