# Imports
import pandas as pd
import pandas_ta as ta
import warnings

# Loca Imports
from db.database import database
from backtest.strat.strategy import strategy
from backtest.strat.settings.settings import settings
from backtest.strat.indicator import indicator
from backtest.backtester import Backtester
from lib.cli.printer import *
from lib.cli.listener import *

from backtest.strat.agent import *

# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Ignoring future warning initially
warnings.simplefilter(action='ignore',category=FutureWarning)
start = 1546300800
end = 1672531200


