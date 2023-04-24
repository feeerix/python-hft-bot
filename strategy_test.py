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


# ema21_setting = settings("ema21", "ema", {'length': 21})
# ema144_setting = settings("ema144", "ema", {'length': 144})
# bollingerband_setting = settings("bbands21", "bbands", {'length': 21, "std": 2.0, "mamode": "ema"})

# bullish_ema233 = settings("above_ema144", "above", {"series_a": "close", "series_b": "EMA_144"})
# close_above21 = settings("closeabove21", "above", {"series_a": "close", "series_b": "EMA_21"})

# close_abovebb = settings("close_belowbb", "above", {"series_a": "close", "series_b": "BBU_21_2.0"})
# close_belowbb = settings("close_abovebb", "below", {"series_a": "close", "series_b": "BBL_21_2.0"})

start = 1609502400
end = 1672531200
df = database(verbose=True).kline_df('ETHUSDT', '1h', start, end)
test_strat = strategy("test_meanreversion", df, retreive=True)


# test_strat.add_indicator(indicator(ema21_setting))
# test_strat.add_indicator(indicator(ema144_setting))
# test_strat.add_indicator(indicator(bollingerband_setting))
# test_strat.add_indicator(indicator(close_above21))
# test_strat.add_indicator(indicator(close_abovebb))
# test_strat.add_indicator(indicator(close_belowbb))
# test_strat.add_indicator(indicator(bullish_ema233))

# long1 = settings("long1","long",{"open": {True: ["close_B_BBL_21_2.0", "close_A_EMA_144"],False:[]}, "close":{True:[],False:[]}})
# short1 = settings("short1","short",{"open":{True:["close_A_BBU_21_2.0"],False:["close_A_EMA_144"]}, "close":{True:[],False:[]}})

# long1_close = settings("long1_close","long",{"open":{True:[],False:[]}, "close":{True:["close_A_EMA_21"],False:[]}})
# short1_close = settings("short1_close","short",{"open":{True:[],False:[]}, "close":{True:[],False:["close_A_EMA_21"]}})

# test_strat.add_entry(long1)
# test_strat.add_entry(short1)
# test_strat.add_close(long1_close)
# test_strat.add_close(short1_close)

# test_strat.write_settings()

# Backtester().test_strat()

bt = Backtester(verbose=True)

# bt.test_run(bt.init_test_strat())
bt.test_run(test_strat)
exit()
