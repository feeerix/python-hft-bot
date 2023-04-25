# Imports
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import plotly.express as px
import inspect
import numpy as np
import warnings
from datetime import datetime

# Loca Imports
from db.db import database
from backtest.strat.strat import strategy
from backtest.strat.settings.settings import settings
from backtest.strat.indicator import indicator
from backtest.strat.composer import get_required_params
# from backtest.backtester import Backtester

pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# -------------------
# Trying to do everything manually
# -------------------

# Ignoring future warning initially
warnings.simplefilter(action='ignore',category=FutureWarning)


# Backtester().test_strat()
# exit()
stochrsi_setting = settings("stochrsi", "stochrsi", {'length':21,'rsi_length':21,'k':5,'d':5}, verbose=False)
ema8_setting = settings("ema8", "ema", {'length': 8}, verbose=False)
ema21_setting = settings("ema21", "ema", {'length': 21}, verbose=False)
ema144_setting = settings("ema144", "ema", {'length': 144}, verbose=False)
ema233_setting = settings("ema233", "ema", {'length': 233}, verbose=False)

atr_setting = settings("atr", "atr", {'length':21}, verbose=False)

start = 1640995200
end = 1672531200
df = database().kline_df('ETHUSDT', '4h', start, end)
test_strat = strategy("test", df)

test_strat.add_indicator(indicator(stochrsi_setting))
test_strat.add_indicator(indicator(ema8_setting))
test_strat.add_indicator(indicator(ema21_setting))
test_strat.add_indicator(indicator(ema144_setting))
test_strat.add_indicator(indicator(ema233_setting))
test_strat.add_indicator(indicator(atr_setting))

cond_8above21_setting = settings("8above21", "above", {'series_a':'EMA_8','series_b':'EMA_21'}, verbose=False)
cond_8below21_setting = settings("8below21", "below", {'series_a':'EMA_8','series_b':'EMA_21'}, verbose=False)

cond_144above233_setting = settings("144above233", "above", {'series_a':'EMA_144','series_b':'EMA_233'}, verbose=False)
cond_144below233_setting = settings("144below233", "below", {'series_a':'EMA_144','series_b':'EMA_233'}, verbose=False)

test_strat.add_indicator(indicator(cond_8above21_setting))
test_strat.add_indicator(indicator(cond_8below21_setting))

test_strat.add_indicator(indicator(cond_144above233_setting))
test_strat.add_indicator(indicator(cond_144below233_setting))

stoch_bull = settings("stochrsi_bull", "cross", {'series_a':'STOCHRSIk_21_21_5_5','series_b':'STOCHRSId_21_21_5_5', 'above':True}, verbose=False)
stoch_bear = settings("stochrsi_bear", "cross", {'series_a':'STOCHRSIk_21_21_5_5','series_b':'STOCHRSId_21_21_5_5', 'above':False}, verbose=False)

test_strat.add_indicator(indicator(stoch_bull))
test_strat.add_indicator(indicator(stoch_bear))


long1 = settings("long1","long",{"open": {True: ["EMA_8_B_EMA_21", "EMA_144_A_EMA_233", "STOCHRSIk_21_21_5_5_XA_STOCHRSId_21_21_5_5"],False:[]}, "close":{True:[],False:[]}})
short1 = settings("short1","short",{"open":{True:["EMA_8_A_EMA_21", "EMA_144_B_EMA_233", "STOCHRSIk_21_21_5_5_XB_STOCHRSId_21_21_5_5"],False:[]}, "close":{True:[],False:[]}})

long1_close = settings("long1_close","long",{"open":{True:[],False:[]}, "close":{True:[],False:["EMA_8_B_EMA_21", "EMA_144_A_EMA_233"]}})
short1_close = settings("short1_close","short",{"open":{True:[],False:[]}, "close":{True:[],False:["EMA_8_A_EMA_21", "EMA_144_B_EMA_233"]}})

test_strat.add_entry(long1)
test_strat.add_entry(short1)
test_strat.add_close(long1_close)
test_strat.add_close(short1_close)

# long1close = settings("long1_close", "")

# print(test_strat.df.columns.to_list())
# long_count = 0
# short_count = 0
# for x in range(len(test_strat.df)):
#     if test_strat.df['long1'].iloc[x] == 1:
#         long_count += 1
#     if test_strat.df['short1'].iloc[x] == 1:
#         short_count += 1


print(test_strat.df)
print('---'*32)
exit()