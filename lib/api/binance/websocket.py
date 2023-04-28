# IMPORTS
import websocket
import json

# LOCAL IMPORTS
from ..ws_gopher import ws_gopher

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

ws_urls = [
    "wss://data-stream.binance.com:9443/ws",
    "wss://stream.binance.com:443/ws",
    "wss://stream.binance.com:9443/ws"
]

ws = websocket.WebSocket()
ws_url = "wss://data-stream.binance.com:9443/ws"
headers = []


class ws_agent(ws_gopher):
    def __init__(self): 
        super().__init__('binance')

    def connect(self, option:int):
        super().connect(ws_urls[option])
    
    def subscribe(self, stream_type:str):
        pass

    

    def send(self, method:str, params:list):
        self.ws.send(
            json.dumps(
                {
                    "method": method,
                    "params": params,
                    "id": 1
                }
            )
        )

    def connect(self):
        ws = websocket.create_connection(ws_url)
        
        ws.send(
            json.dumps(
                {
                "method": "SUBSCRIBE",
                "params":
                [
                    "ethusdt@kline_1m"
                ],
                "id": 1
                }
            )
        )
        counter = 0
        while True:
            response = ws.recv()
            print(f"RESPONSE: {response}")
            counter += 1
            if counter > 10:
                exit()