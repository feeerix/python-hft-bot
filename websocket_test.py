# Imports
import time

# Local Imports
# from lib.api.updater import update
from lib.api.binance.websocket import ws_agent
# from lib.api.binance.interface import Binance
from lib.tools.exchange import ExchangeType
from lib.cli.printer import line
# from lib.file.reader import get_json


# # pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)
# pd.set_option('display.float_format', lambda x: '%.5f' % x)

# # -------------------
# # Trying to do everything manually
# # -------------------

# # Ignoring future warning initially
# warnings.simplefilter(action='ignore',category=FutureWarning)

# --------------------------------------------------------------------------------------------

# Create the corresponding class
websocket_agent = ws_agent(ExchangeType.BINANCE, verbose=True)

# Connect based on URL
websocket_agent.create_connection()

# Subscribe to the right stream


# Start the loop


websocket_agent.subscribe(
    {
        "stream_type": "kline",
        "symbol": "ethusdt",
        "interval": "1m"
    }
)

counter = 0
while True:
    response = websocket_agent.receive_data()
    print(response)

    if counter > 10:
        websocket_agent.close_connection()
        break
exit()

# --------------------------------------------------------------------------------------------
websocket_agent = ws_agent(verbose=True)
websocket_agent.create_connection(0)

websocket_agent.subscribe(
    {
        "stream_type": "depth",
        "symbol": "ethusdt",
        "level": "0"
    }
)

counter = 0
time.sleep(0.1)
api_response = Binance().api_request('depth', {"symbol": "ETHUSDT", "limit":100})

print(api_response)

print(line)
print(f"LAST UPDATED: {api_response['lastUpdateId']}")

print(line)

ws_data = []
matched = False
while True:
    response = websocket_agent.receive_data()
    # print(f"Last update id: {response['data']['lastUpdateId']}")
    
    counter += 1

    if response:
        if 'u' in response:
            ws_data.append(response)
            # print(f"last update id: {response['u']} - from WS")
            # print(f"last update id: {api_response['lastUpdateId']} - from API")

            if response['u'] <= api_response['lastUpdateId']:
                print(f"DROPPED")
            elif matched is False:
                if response['U'] <= (api_response['lastUpdateId'] + 1) and response['u'] >= (api_response['lastUpdateId'] + 1):
                    print(f"MATCHED - {response['u']}")
                    matched = True
                    print(line)
        else:
            print(response)

    if counter >= 100:
        print(line)
        print(f"COUNTER LIMIT HIT")
        websocket_agent.close_connection()
        break
