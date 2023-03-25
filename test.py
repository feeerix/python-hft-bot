# Imports
import pandas as pd
import pandas_ta as ta

# Local Imports
# from backtest.backtester import Backtester
from db.db import database

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Test object

# print(ta.ema.__code__.co_varnames)
# print(ta.bbands__code__.co_varnames)


# Backtester().test_strat()
df = database().kline_df('ETHUSDT', '4h', 1640995200, 1672531200)
# df = database().kline_df('ETHUSDT', '1m', 1640995200, 1640995300)

# df[['k','d']] = ta.stochrsi(close=df['close'], length=21, rsi_length=21, k=5, d=5)
# df['ema233'] = ta.ema()
# print(ta.cross(df['k'],df['d']))

df['qa_vol/vol'] = df['quote_volume'] / df['volume']

print(df)

# ohlc4 = (df['open'].iloc[0] + df['high'].iloc[0] + df['low'].iloc[0] + df['close'].iloc[0])/4
# print(f"ohlc4: {ohlc4}")
# print(f"Quote Volume: {df['quote_volume'].iloc[0] / df['volume'].iloc[0]}")
# print(df['taker_buy_volume'].iloc[0] + df['taker_quote_volume'].iloc[0])