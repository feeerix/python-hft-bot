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

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Ignoring future warning initially
warnings.simplefilter(action='ignore',category=FutureWarning)


stochrsi_setting = settings("test", "stochrsi", {'window':21,'smooth_k':5,'smooth_d':5}, verbose=False)
ema21_setting = settings("ema21", "ema", {'length': 21}, verbose=False)
ema144_setting = settings("ema144", "ema", {'length': 144}, verbose=False)
ema233_setting = settings("ema233", "ema", {'length': 233}, verbose=False)


start = 1640995200
end = 1672531200
df = database().kline_df('ETHUSDT', '1m', start, end)

test_strat = strategy("test_strategy",False)
test_strat.init_df(df)
test_strat.add_indicator(indicator(stochrsi_setting))
test_strat.add_indicator(indicator(ema21_setting))
test_strat.add_indicator(indicator(ema144_setting))
test_strat.add_indicator(indicator(ema233_setting))

print(get_required_params('above'))

# print(ta.above(test_strat.df['EMA_144'],test_strat.df['EMA_233']))

# print(test_strat.df)

# test_settings = settings("test", "stochrsi", {'window':21,'smooth_k':5,'smooth_d':5}, verbose=False)
# test2_settings = settings("test2", "ema", {'length': 21}, verbose=False)
# test_indicator = indicator(test_settings)
# test2_indicator = indicator(test2_settings)
# df = database().kline_df('ETHUSDT', '4h', 1640995200, 1672531200)
# test_result = test_indicator.ret_indicator(df)
# test2_result = test2_indicator.ret_indicator(df)
# print(df)
# print(pd.concat([test_result, test2_result], axis=1 ,ignore_index=True))



exit()
