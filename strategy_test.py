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

start = 1609502400
end = 1672531200
df = database(verbose=True).kline_df('ETHUSDT', '1h', start, end)

# Create method to create strategies easily
test_strat = strategy("test_00", df, retreive=False)

# First we add the indicators that we want to have as columns in our df
test_strat.add_indicator

# ---
# FIND A WAY TO CREATE STRATEGIES
# ---


bt = Backtester(verbose=True)



# bt.test_run(bt.init_test_strat())
test_strat.write_settings()
bt.test_run(test_strat, 5000)
exit()
