# Imports
import pandas as pd

# Local Imports
from backtest.backtester import Backtester
from db.db import database

# Test object
Backtester().test_strat()
# database.test_create_df('ETHUSDT','1m',1640995200, 1672531200)