# Imports
import pandas as pd
import pandas_ta as ta
import warnings
from datetime import datetime

# Loca Imports
from lib.api.binance.binance import Binance
from db.database import Database, DatabaseType
from lib.tools.symbol import Symbol
from lib.tools.interval import _Interval as Interval
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

test_binance = Binance()

# Database().kline_df('ETHUSDT',"4h",start,end)
eth = Asset("Ethereum", "ETH", "0x0", AssetType.COIN, Network.ETHEREUM)
usdt = Asset("Tether", "USDT", "0x0", AssetType.TOKEN, Network.ETHEREUM)

ethusdt = Symbol("ETHUSDT", [eth, usdt])
interval1 = str(Interval._4h)
# interval2 = str(Interval._1m)

"""
Currently, what I'm working through is that a strategy is VERY likely going to need more than one database potentially.
Is it more efficient to have the database in memory, as a dataframe or would it be better to try to access the corresponding data ad hoc?
At the moment, experimenting with allowing the strategy to have more than one 'database'.

Instead of inputting the dataframe into the strategy, it's probably a better idea for the strategy to not even need a dataframe (as not all strategies require that
you define what assets you're interacting with.).

For example, if I wanted to hotswap a strategy between two datasets (and therefore check the correlation between the two assets and if my strategy works between then
I should be able to do so.)

"""



# df2 = Database(verbose=True)._kline_df(ethusdt, interval2, start, end)

test_strat = Strategy(
    name="test1", 
    klines=Database(db_type=DatabaseType.KLINES),
    indicators=Database(db_type=DatabaseType.INDICATORS),
    orderbook=Database(db_type=DatabaseType.ORDERBOOK),
    signals=Database(db_type=DatabaseType.SIGNALS),
    logic=Database(db_type=DatabaseType.LOGIC),
    positions=Database(db_type=DatabaseType.POSITIONS),
    verbose=True,
)
# test_strat2 = Strategy("test2", df2)

# ema8 = Indicator(Settings("ema8", "ema", {'length': 8}))
# ema21 = Indicator(Settings("ema21", "ema", {'length': 21}))
# ema144 = Indicator(Settings("ema144", "ema", {'length': 144}))
# ema233 = Indicator(Settings("ema233", "ema", {'length': 233}))
# stochrsi = Indicator(Settings("stochrsi", "stochrsi", {"length": 21, "rsi_length": 21, "k": 5, "d": 5}))

# test_strat.add_indicator(ema8)
# test_strat.add_indicator(ema21)
# test_strat.add_indicator(ema144)
# test_strat.add_indicator(ema233)
# test_strat.add_indicator(stochrsi)



# test_strat2.add_indicator(ema8)
# test_strat2.add_indicator(ema21)
# test_strat2.add_indicator(ema144)
# test_strat2.add_indicator(ema233)
# test_strat2.add_indicator(stochrsi)


"""
Now that we have created both dataframes as well as added the indicators, let's see if we want to perform the modelling within the strategy class?
"""

