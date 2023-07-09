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

# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# -------------------
# Trying to do everything manually
# -------------------

# Ignoring future warning initially
warnings.simplefilter(action='ignore',category=FutureWarning)
# start = 1546300800
start = 1569888000 # ETH / BTC
# start = 1568880000

# start = 1527480000 # XRP BUSD
# start = 1609502400
end = 1672531200
# end = 1672531200
df = database(verbose=True).kline_df('ETHUSDT', '1h', start, end)

# Create method to create strategies easily
test_strat = strategy("default", df, retreive=False)

# MAIN COLUMNS
# ------------------------------------------------------------
# EMA
ema8_setting = settings("ema8", "ema", {'length': 8})
ema21_setting = settings("ema21", "ema", {'length': 21})
ema144_setting = settings("ema144", "ema", {'length': 144})
ema233_setting = settings("ema233", "ema", {'length': 233})

test_strat.add_indicator(indicator(ema8_setting))
test_strat.add_indicator(indicator(ema21_setting))
test_strat.add_indicator(indicator(ema144_setting))
test_strat.add_indicator(indicator(ema233_setting))

stochrsi_setting = settings("stochrsi", "stochrsi", {"length": 34, "rsi_length": 34, "k": 8, "d": 8})
test_strat.add_indicator(indicator(stochrsi_setting))

atr_setting = settings("atr", "atr", {"length": 21, "mamode": "ema"}, transform={"band": 2})
test_strat.add_indicator(indicator(atr_setting))

"""
To Effectively "build" strategies, I will need to better abstract and automate the process, such that I could do it from the command line.

"""



# ------------------------------------------------------------
# CONDITIONAL COLUMNS

"""
First Bullish position:
EMA 144 > EMA 233 -> Bullish overall trend
EMA8 < EMA 21 -> Small reversion

Stochastic RSI (k & d) < 20 -> Oversold short term
Stochastic RSI bullish cross ->  Trigger

Stochastic RSI (k & d) > 80 -> Overbought short term
Stochastic RSI bearish cross ->  Trigger

TP -> 3 x ATR
SL -> 2 x ATR 

Opposite for bearish
"""

bullish_ema144_ema233 = settings("144Above233_bullish", "above", {"series_a": "EMA_144", "series_b": "EMA_233"})
bearish_ema144_ema233 = settings("144Below233_bearish", "below", {"series_a": "EMA_144", "series_b": "EMA_233"})
bearish_ema8_ema21 = settings("ema8below_ema21", "below", {"series_a": "EMA_8", "series_b": "EMA_21"})
bullish_ema8_ema21 = settings("ema8above_ema21", "above", {"series_a": "EMA_8", "series_b": "EMA_21"})

test_strat.add_indicator(indicator(bullish_ema144_ema233))
test_strat.add_indicator(indicator(bearish_ema144_ema233))
test_strat.add_indicator(indicator(bullish_ema8_ema21))
test_strat.add_indicator(indicator(bearish_ema8_ema21))

stochrsi_oversold_k = settings("stochrsi_oversold_k", "below_value", {"series_a": "STOCHRSIk_34_34_8_8", "value": 20.0})
stochrsi_oversold_d = settings("stochrsi_oversold_d", "below_value", {"series_a": "STOCHRSId_34_34_8_8", "value": 20.0})
stochrsi_overbought_k = settings("stochrsi_overbought_k", "above_value", {"series_a": "STOCHRSIk_34_34_8_8", "value": 80.0})
stochrsi_overbought_d = settings("stochrsi_overbought_d", "above_value", {"series_a": "STOCHRSId_34_34_8_8", "value": 80.0})

test_strat.add_indicator(indicator(stochrsi_oversold_k))
test_strat.add_indicator(indicator(stochrsi_oversold_d))
test_strat.add_indicator(indicator(stochrsi_overbought_k))
test_strat.add_indicator(indicator(stochrsi_overbought_d))

stochrsi_bullish_trigger = settings("stochrsi_bullcross", "cross", {"series_a": "STOCHRSIk_34_34_8_8", "series_b": "STOCHRSId_34_34_8_8"})
stochrsi_bearish_trigger = settings("stochrsi_bullcross", "cross", {"series_a": "STOCHRSIk_34_34_8_8", "series_b": "STOCHRSId_34_34_8_8", "above": False})

test_strat.add_indicator(indicator(stochrsi_bullish_trigger))
test_strat.add_indicator(indicator(stochrsi_bearish_trigger))

# <<<<<<< HEAD
# =======

# >>>>>>> 352442bdff94838c27720307d1bee356e9f606a4
long1 = settings(
    "long1",
    "long",
    {
        "open": {True: ["EMA_144_A_EMA_233", "EMA_8_B_EMA_21", "STOCHRSIk_34_34_8_8_B_20_0", "STOCHRSId_34_34_8_8_B_20_0", "STOCHRSIk_34_34_8_8_XA_STOCHRSId_34_34_8_8"],False:[]}, 
        "close":{True:["EMA_144_B_EMA_233", "STOCHRSIk_34_34_8_8_B_20_0", "STOCHRSId_34_34_8_8_B_20_0"],False:[]}
    }
)
        
short1 = settings("short1","short",{"open":{True:["STOCHRSIk_34_34_8_8_A_80_0", "STOCHRSId_34_34_8_8_A_80_0", "STOCHRSIk_34_34_8_8_XB_STOCHRSId_34_34_8_8", "EMA_144_B_EMA_233", "EMA_8_B_EMA_21"],False:[]}, "close":{True:[],False:[]}})

short1 = settings(
    "short1",
    "short",
    {
        "open":{True:["STOCHRSIk_34_34_8_8_A_80_0", "STOCHRSId_34_34_8_8_A_80_0", "STOCHRSIk_34_34_8_8_XB_STOCHRSId_34_34_8_8", "EMA_144_B_EMA_233", "EMA_8_B_EMA_21"],False:[]}, 
        "close":{True:["EMA_144_A_EMA_233", "STOCHRSIk_34_34_8_8_A_80_0", "STOCHRSId_34_34_8_8_A_80_0"],False:[]}
    }
)



# long1_close = settings("long1_close","long",{"open":{True:[],False:[]}, "close":{True:["EMA_144_B_EMA_233", "STOCHRSIk_34_34_8_8_B_20_0", "STOCHRSId_34_34_8_8_B_20_0"],False:[]}})
# short1_close = settings("short1_close","short",{"open":{True:[],False:[]}, "close":{True:["EMA_144_A_EMA_233", "STOCHRSIk_34_34_8_8_A_80_0", "STOCHRSId_34_34_8_8_A_80_0"],False:[]}})

# We are now adjusting how the settings
test_strat.add_entry(long1)
test_strat.add_entry(short1)
# test_strat.add_close(long1_close)
# test_strat.add_close(short1_close)

# ---
# FIND A WAY TO CREATE STRATEGIES
# ---


bt = Backtester(verbose=True)



# bt.test_run(bt.init_test_strat())
# test_strat.write_settings()
print(line)
# print(test_strat.df.columns.to_list())
# <<<<<<< HEAD
bt.test_runv0(test_strat, 1000)
# print(test_strat.df.columns.to_list())
# =======
# bt.test_runv1(test_strat, 1000)
print(test_strat.df.columns.to_list())
# >>>>>>> 352442bdff94838c27720307d1bee356e9f606a4

"""
Get List of indicators

"""

exit()
