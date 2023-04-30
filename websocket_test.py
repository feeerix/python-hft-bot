# Imports
import time

# Local Imports
from lib.api.updater import update
from lib.api.binance.websocket import ws_agent
from lib.api.binance.interface import Binance
from lib.cli.printer import line
# from lib.file.reader import get_json


# # pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# # pd.set_option('display.width', None)
# # pd.set_option('display.max_colwidth', None)
# pd.set_option('display.float_format', lambda x: '%.5f' % x)

# # -------------------
# # Trying to do everything manually
# # -------------------

# # Ignoring future warning initially
# warnings.simplefilter(action='ignore',category=FutureWarning)

# ws = websocket.WebSocket()
# ws_url = "wss://stream.binance.com:9443/ws/ETHUSDT@kline_1m/"
# ws.connect(ws_url)

# Pair
pair_list = ['ETHUSDT']

# Intervals
interval_list = ['1m']
# update('Binance', pair_list, interval_list)

# Manually get depth snapshot?



websocket_agent = ws_agent(verbose=True)
websocket_agent.create_connection(0)
websocket_agent.subscribe(
    {
        "stream_type": "depth",
        "symbol": "ethusdt",
        "level": str(20)
    }
)

counter = 0

time.sleep(0.1)

response = Binance().api_request('depth', {"symbol": "ETHUSDT", "limit":100})
print(f"LAST UPDATED: {response['lastUpdateId']}")
print(line)
ws_data = []
while True:
    ws_data.append(websocket_agent.receive_data()['data'])
    
    counter += 1
    if len(ws_data) > 1:    
        
        if response['lastUpdateId'] == ws_data[-1]['lastUpdateId'] | counter > 100:

            websocket_agent.close_connection()
            print(ws_data)
            print(response)
            print(f"MATCHED AT TIME: {response['lastUpdateId']}")
            print(line)
            break
