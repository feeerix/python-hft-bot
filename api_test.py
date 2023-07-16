# Imports
import pandas as pd
import pandas_ta as ta
import warnings

# Loca Imports
# from lib.api.binance import

from lib.api.binance.binance import Binance
from lib.tools.exchange import ExchangeType
from lib.file.reader import get_json

# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Ignoring future warning initially
warnings.simplefilter(action='ignore',category=FutureWarning)
start = 1546300800
end = 1672531200

test_binance = Binance()
result = test_binance.get_info()
print(result)
