# Imports
import pandas as pd
import pandas_ta as ta
import warnings

# Loca Imports
from db.database import Database, DatabaseType
from lib.tools.symbol import Symbol
from lib.tools.exchange import ExchangeType
from lib.tools.interval import Interval
from lib.tools.asset import Asset, AssetType
from lib.tools.network import Network
from backtest.strat.signal import Signal
from backtest.strat.strategy import Strategy
from backtest.strat.indicator import Indicator
from backtest.strat.settings.settings import Settings
from backtest.backtester import Backtester
from lib.cli.printer import *
from lib.cli.listener import *

# Imports
import pandas as pd
import pandas_ta as ta
import warnings
from datetime import datetime

# Local Imports
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

klines_4h = Database("", DatabaseType.KLINES, True, symbol=ethusdt, interval=Interval._4h, starttime=start, endtime=end, source=ExchangeType.BINANCE)
klines_1h = Database("", DatabaseType.KLINES, True, symbol=ethusdt, interval=Interval._1h, starttime=start, endtime=end, source=ExchangeType.BINANCE)
klines_15m = Database("", DatabaseType.KLINES, True, symbol=ethusdt, interval=Interval._15m, starttime=start, endtime=end, source=ExchangeType.BINANCE)
klines_5m = Database("", DatabaseType.KLINES, True, symbol=ethusdt, interval=Interval._5m, starttime=start, endtime=end, source=ExchangeType.BINANCE)
klines_1m = Database("", DatabaseType.KLINES, True, symbol=ethusdt, interval=Interval._1m, starttime=start, endtime=end, source=ExchangeType.BINANCE)

indicator_list = [
    Indicator(Settings("ema8", "ema", {'length': 8})),
    Indicator(Settings("ema21", "ema", {'length': 21})),
    Indicator(Settings("ema144", "ema", {'length': 144})),
    Indicator(Settings("ema233", "ema", {'length': 233})),
    Indicator(Settings("stochrsi", "stochrsi", {"length": 21, "rsi_length": 21, "k": 5, "d": 5})),
    Indicator(Settings("atr", "atr", {"length": 21, "mamode": "ema"}))
]


"""
This is a database of the indicators that are going to be used for a 
particular timeframe interval
"""
indicators_4h = Database(
    "", # Name
    DatabaseType.INDICATORS, # To list that this is a database of indicators
    True, # Verbosity
    symbol=[ethusdt], # Symbol indicators relate to
    interval=[Interval._4h], # Interval it relates to
    indicators=indicator_list, # The list of indicators to be added
    recording=False # If I'm recording and saving the data,
    )

indicators_1h = Database(
    "", # Name
    DatabaseType.INDICATORS, # To list that this is a database of indicators
    True, # Verbosity
    symbol=[ethusdt], # Symbol indicators relate to
    interval=[Interval._1h], # Interval it relates to
    indicators=indicator_list, # The list of indicators to be added
    recording=False # If I'm recording and saving the data,
    )

indicators_15m = Database(
    "", # Name
    DatabaseType.INDICATORS, # To list that this is a database of indicators
    True, # Verbosity
    symbol=[ethusdt], # Symbol indicators relate to
    interval=[Interval._15m], # Interval it relates to
    indicators=indicator_list, # The list of indicators to be added
    recording=False # If I'm recording and saving the data,
    )

indicators_5m = Database(
    "", # Name
    DatabaseType.INDICATORS, # To list that this is a database of indicators
    True, # Verbosity
    symbol=[ethusdt], # Symbol indicators relate to
    interval=[Interval._5m], # Interval it relates to
    indicators=indicator_list, # The list of indicators to be added
    recording=False # If I'm recording and saving the data,
    )

indicators_1m = Database(
    "", # Name
    DatabaseType.INDICATORS, # To list that this is a database of indicators
    True, # Verbosity
    symbol=[ethusdt], # Symbol indicators relate to
    interval=[Interval._1m], # Interval it relates to
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
    klines_1h, 
    # klines_15m, 
    # klines_5m, 
    # klines_1m
]

indicator_dbs = [
    indicators_4h,
    indicators_1h,
    indicators_15m,
    indicators_5m,
    indicators_1m
]

"""
Important question now is how we get the specific signals. At the moment, it is currently
manually input, as you can see. We should be able to select from the currently available 
columns to select what is above another etc.
"""


signal_indicators = [
    Signal(Settings("144Above233_bullish", "above", {"series_a": "EMA_144", "series_b": "EMA_233"}), Interval._4h),
    Signal(Settings("144Below233_bearish", "below", {"series_a": "EMA_144", "series_b": "EMA_233"}), Interval._4h),
    Signal(Settings("ema8below_ema21", "below", {"series_a": "EMA_8", "series_b": "EMA_21"}), Interval._4h),
    Signal(Settings("ema8above_ema21", "above", {"series_a": "EMA_8", "series_b": "EMA_21"}), Interval._4h),
    Signal(Settings("stochrsi_oversold_k", "below_value", {"series_a": "STOCHRSIk_21_21_5_5", "value": 20.0}), Interval._4h),
    Signal(Settings("stochrsi_oversold_d", "below_value", {"series_a": "STOCHRSId_21_21_5_5", "value": 20.0}), Interval._4h),
    Signal(Settings("stochrsi_overbought_k", "above_value", {"series_a": "STOCHRSIk_21_21_5_5", "value": 80.0}), Interval._4h),
    Signal(Settings("stochrsi_overbought_d", "above_value", {"series_a": "STOCHRSId_21_21_5_5", "value": 80.0}), Interval._4h),
    Signal(Settings("stochrsi_bullcross", "cross", {"series_a": "STOCHRSIk_21_21_5_5", "series_b": "STOCHRSId_21_21_5_5"}), Interval._4h),
    Signal(Settings("stochrsi_bullcross", "cross", {"series_a": "STOCHRSIk_21_21_5_5", "series_b": "STOCHRSId_21_21_5_5", "above": False}), Interval._4h)
]
# def __init__(self, name:str="", db_type:DatabaseType=None, verbose:bool=False, **kwargs):
signal_dbs = Database("Signal database", DatabaseType.SIGNALS, True, signals=signal_indicators)

portfolio_db = Database(db_type=DatabaseType.PORTFOLIO, symbols=[])

test_strat = Strategy(
    name="test1",
    portfolio=Database(db_type=DatabaseType.PORTFOLIO),
    klines=klines_dbs,
    indicators=indicator_dbs,
    orderbook=[Database(db_type=DatabaseType.ORDERBOOK)], # TODO - need to update exchange class to add ws functions
    signals=signal_dbs,
    logic=Database(db_type=DatabaseType.LOGIC),
    positions=Database(db_type=DatabaseType.POSITIONS),
    verbose=True,
)

print("CREATED TEST STRAT")
test_strat.build()



# ---
# FIND A WAY TO CREATE STRATEGIES
# ---


bt = Backtester(verbose=True)

print(line)

# def test_runv0(self, test_strat:strategy, capital:float, run_settings:settings=None, exchange_settings:settings=None, settings_write:bool=False):
# bt.test_runv0(test_strat, 1000, exchange_settings=exchange_settings)
bt.backtest(test_strat, 1000)
# print(test_strat.df.columns.to_list())


exit()