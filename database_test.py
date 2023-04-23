# Imports
import pandas as pd
import pytz
import pandas_ta as ta
import plotly.graph_objects as go
import plotly.express as px
import inspect
import numpy as np
import warnings
from datetime import datetime

# Loca Imports
from db.db import database
# from backtest.strat.strat import strategy
# from backtest.strat.settings.settings import settings
# from backtest.strat.indicator import indicator
# from backtest.strat.composer import get_required_params
# from backtest.backtester import Backtester

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# start = 1640995200
# end = 1672531200
# df = database(verbose=True).kline_df('ETHUSDT','15m',start,end)
# print(f"FIRST VALUE: {df['time'].iloc[0]} // {datetime.fromtimestamp(int(df['time'].iloc[0]/1000), tz=pytz.UTC)}")
# print(f"LAST VALUE: {df['time'].iloc[-1]} // {datetime.fromtimestamp(int(df['time'].iloc[-1]/1000), tz=pytz.UTC)}")
# print(int(df['time'].iloc[-1]/1000))

start = 1641998800
end = 1662526700
df = database(verbose=True).kline_df('ETHUSDT','15m',start,end)
print(f"FIRST VALUE: {df['time'].iloc[0]} // {datetime.fromtimestamp(int(df['time'].iloc[0]/1000), tz=pytz.UTC)}")
print(f"LAST VALUE: {df['time'].iloc[-1]} // {datetime.fromtimestamp(int(df['time'].iloc[-1]/1000), tz=pytz.UTC)}")