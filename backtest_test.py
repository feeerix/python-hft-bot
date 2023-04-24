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
from backtest.backtester import Backtester
from backtest.strat.strat import strategy
from db.db import database

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Ignoring future warning initially
warnings.simplefilter(action='ignore',category=FutureWarning)

# start = 1640995200
start = 1609502400
end = 1672531200
df = database(verbose=True).kline_df('ETHUSDT', '15m', start, end)
# test_strat = strategy("test")
# test_strat.init_df(df)


# Backtester().test_strat()
bt = Backtester(verbose=True)

# bt.test_run(bt.init_test_strat())
bt.test_run(strategy("test",df,retreive=True))