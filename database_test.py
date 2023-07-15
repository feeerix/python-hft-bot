# Imports
import pandas as pd
from datetime import datetime, timezone

# Loca Imports
from db.database import Database
from db.database import _Database as DatabaseV2
from lib.tools.internal.chunk import Chunk
from lib.tools.internal.crawler import Crawler

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

start = 1569888000
end = 1685592000

"""
First we are looking to update the way we handle dataframes.
Let's also try to clean everything up and make everything more performant.

"""

test_crawler = Crawler()
test_crawler.verify_kline()

# --------------------------------------------------------------------------------
# df = Database(verbose=True).kline_df('ETHUSDT','1m',start,end)


# print(f"FIRST VALUE: {df['time'].iloc[0]} // {datetime.fromtimestamp(int(df['time'].iloc[0]/1000), tz=timezone.utc)}")
# print(f"LAST VALUE: {df['time'].iloc[-1]} // {datetime.fromtimestamp(int(df['time'].iloc[-1]/1000), tz=timezone.utc)}")