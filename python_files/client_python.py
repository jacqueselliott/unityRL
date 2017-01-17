from __future__ import division
import websocket
import thread
import sys

queue_received = []

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("Server killed the connection :'(")

def on_open(ws):
    ws.send("Startup!")
    print("Server started!")

def send_message(msg):
    ws.send(msg)

ws = None
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:9001",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()