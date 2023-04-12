# Imports
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import plotly.express as px
import inspect

# Loca Imports
from db.db import database
from backtest.strat.settings.settings import settings
from backtest.strat.indicator import indicator, get_params, write_params

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
# Get a list of all the functions in the pandas_ta module





# ta_funcs = inspect.getmembers(ta, inspect.isfunction)
# for x in ta_funcs:
#     print(x[0])

#     all_params = x[1].__code__.co_varnames
    
#     print(all_params)


# print(ta.ema.__code__.co_varnames)
# print(ta.bbands.__code__.co_varnames)

# test_indicator = indicator()
# Backtester().test_strat()
write_params()
exit()
df = database().kline_df('ETHUSDT', '4h', 1640995200, 1672531200)
# print(df)
df[['k', 'd']] = ta.stochrsi(df['close'],window=21,smooth_k=5,smooth_d=5)
print(df)
# self.db[['stoch_rsi_k', 'stoch_rsi_d']] = ta.stochrsi(self.db['close'],window=14,smooth_k=3,smooth_d=3)

# df[['k','d']] = ta.stochrsi(close=df['close'], length=21, rsi_length=21, k=5, d=5)
# df['ema21'] = ta.ema(close=df['close'],length=21,talib=False)
# df['ema144'] = ta.ema(close=df['close'],length=144,talib=False)


# fig = px.histogram(df['testdiff'], x='testdiff', nbins=1000)
# fig.show()
# print(df)
# fig = go.Figure(data=[
#     go.Candlestick(
#         x=df['time'],
#         open=df['open'],
#         high=df['high'],
#         low=df['low'],
#         close=df['close']
#     ),
    # go.Scatter(
    #     x=df['time'],
    #     y=df['ema21']
    # ),
    # go.Scatter(
    #     x=df['time'],
    #     y=df['ema144']
    # )
# ])
# fig.update_layout(xaxis_rangeslider_visible=False)
# fig.show()
# df = database().kline_df('ETHUSDT', '1m', 1640995200, 1640995300)


