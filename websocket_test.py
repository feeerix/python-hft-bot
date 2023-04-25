# Imports
import pandas as pd
import pandas_ta as ta
import warnings
import websocket
import json

# Loca Imports
from lib.api.binance.websocket import *

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

ws = websocket.WebSocket()
ws_url = "wss://stream.binance.com:9443/ws/ETHUSDT@kline_1m/"
ws.connect(ws_url)

data = ws.recv()
