import websocket
import json

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