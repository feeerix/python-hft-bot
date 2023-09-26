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
from backtest.strat.trigger import Trigger
from backtest.strat.strategy import Strategy
from backtest.strat.logic import Logic
from backtest.strat.indicator import Indicator
from backtest.strat.settings.settings import Settings
from backtest.backtester import Backtester

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

"""
Important question now is how we get the specific signals. At the moment, it is currently
manually input, as you can see. We should be able to select from the currently available 
columns to select what is above another etc.

Additionally - this will be wha
"""


trigger_indicators = [
    Trigger(Settings("144Above233_bullish", "above", {"series_a": "EMA_144", "series_b": "EMA_233"}), Interval._4h),
    Trigger(Settings("144Below233_bearish", "below", {"series_a": "EMA_144", "series_b": "EMA_233"}), Interval._4h),
    Trigger(Settings("ema8below_ema21", "below", {"series_a": "EMA_8", "series_b": "EMA_21"}), Interval._4h),
    Trigger(Settings("ema8above_ema21", "above", {"series_a": "EMA_8", "series_b": "EMA_21"}), Interval._4h),
    Trigger(Settings("stochrsi_oversold_k", "below_value", {"series_a": "STOCHRSIk_21_21_5_5", "value": 20.0}), Interval._4h),
    Trigger(Settings("stochrsi_oversold_d", "below_value", {"series_a": "STOCHRSId_21_21_5_5", "value": 20.0}), Interval._4h),
    Trigger(Settings("stochrsi_overbought_k", "above_value", {"series_a": "STOCHRSIk_21_21_5_5", "value": 80.0}), Interval._4h),
    Trigger(Settings("stochrsi_overbought_d", "above_value", {"series_a": "STOCHRSId_21_21_5_5", "value": 80.0}), Interval._4h),
    Trigger(Settings("stochrsi_bullcross", "cross", {"series_a": "STOCHRSIk_21_21_5_5", "series_b": "STOCHRSId_21_21_5_5"}), Interval._4h),
    Trigger(Settings("stochrsi_bullcross", "cross", {"series_a": "STOCHRSIk_21_21_5_5", "series_b": "STOCHRSId_21_21_5_5", "above": False}), Interval._4h)
]
# def __init__(self, name:str="", db_type:DatabaseType=None, verbose:bool=False, **kwargs):
trigger_dbs = Database("trigger_db", DatabaseType.TRIGGERS, True, triggers=trigger_indicators)

portfolio_db = Database("portfolio_db", DatabaseType.PORTFOLIO, symbols=[])

logic_blocks = [
    Logic(
        Settings("bullish_long", "long", {
                True:[
                    "EMA_8_B_EMA_21", 
                    "EMA_144_A_EMA_233",
                    "STOCHRSIk_21_21_5_5_XA_STOCHRSId_21_21_5_5",
                    "STOCHRSIk_21_21_5_5_B_20_0",
                    "STOCHRSId_21_21_5_5_B_20_0"
                ],
                False:[
                ]
            }
        ),
        [Interval.from_string('4h')]
    ),
    Logic(
        Settings("bearish_short", "SHORT", {
                True:[
                    "EMA_8_A_EMA_21", 
                    "EMA_144_B_EMA_233",
                    "STOCHRSIk_21_21_5_5_XB_STOCHRSId_21_21_5_5",
                    "STOCHRSIk_21_21_5_5_A_80_0",
                    "STOCHRSId_21_21_5_5_A_80_0"
                ],
                False:[
                ]
            }
        ),
        [Interval.from_string('4h')]
    )
]

logic_db = Database("Logic_db", db_type=DatabaseType.LOGIC, logic=logic_blocks)

test_strat = Strategy(
    name="test1",
    portfolio=portfolio_db,
    klines=klines_dbs,
    indicators=indicator_dbs,
    orderbook=[Database(db_type=DatabaseType.ORDERBOOK)],
    triggers=trigger_dbs,
    logic=logic_db,
    positions=Database(db_type=DatabaseType.POSITIONS),
    verbose=True
)

print("CREATED TEST STRAT")
test_strat.build()
# print(test_strat.klines)

Backtester(verbose=True).backtest(test_strat, 1000)

"""
Next step is to make sure we can implement our signals, and then the logic for trading
Once we have done that, we will add to the positions database, and then create a performance
database, with the corresponding trades (A DB WITHIN DB?!) and then continue from there.
"""

# print(test_strat.klines[0].df)


exit()

"""
Now that we have created both dataframes as well as added the indicators, let's see if we want to perform the modelling within the strategy class?
"""

