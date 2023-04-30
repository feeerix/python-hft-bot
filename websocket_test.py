# Imports
import json

# Local Imports
from lib.api.binance.websocket import ws_agent, return_stream_id, stream_type
from lib.file.reader import get_json

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


def on_message(ws, message):
    data = json.loads(message)
    print(data)
    # process the data

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("Connection closed")

def on_open(ws):
    print("Connection opened")





websocket_agent = ws_agent(verbose=True)
websocket_agent.create_connection(0)
websocket_agent.subscribe(
    {
        "stream_type": "kline",
        "symbol": "ethusdt",
        "interval": "1m"
    }
    # [
    #     "ethusdt@kline_1m"
    #     stream_type('kline', 'ethusdt', '1m')
    # ]
)

counter = 0
while True:
    websocket_agent.receive_data()
    counter += 1
    if counter > 10:
        websocket_agent.close_connection()
        break

# ws = websocket.WebSocket()
# ws_url = "wss://data-stream.binance.com:9443/ws"
# headers = []
# ws = websocket.create_connection(ws_url)
# ws = websocket.WebSocketApp(
#     ws_url,
#     on_open=on_open,
#     on_message=on_message,
#     on_error=on_error,
#     on_close=on_close
# )
# ws.send(
#     json.dumps(
#         {
#         "method": "SUBSCRIBE",
#         "params":
#         [
#             "ETHUSDT@kline_1m"
#         ],
#         "id": 1
#         }
#     )
# )
# print(ws.recv())

# ws.run_forever()
# ws.connect(ws_url)
# ws.send(
#     json.dumps(
#         {
#         "method": "SUBSCRIBE",
#         "params":
#         [
#             "ETHUSDT@kline_1m"
#         ],
#         "id": 1
#         }
#     )
# )

# counter = 0
# while True:
#     response = ws.recv()
#     print(response)
#     counter += 1
#     if counter > 100:
#         exit()