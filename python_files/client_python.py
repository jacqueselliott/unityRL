from __future__ import division
import websocket
import threading
from random import randint
import sys
import q_network_simple_sim

count = 0
data_received = False
data_message = ""

def on_message(ws, message):
    if data_received == False
        data_message = message
        data_received = True

def on_error(ws, error):
    print(error)

def on_close(ws):
    pass

def on_open(ws):
    send_message('client')
    while True:
        print('Type hello to start')
        cur = raw_input()
        if cur == 'hello':
            break
    send_message(str(-1))

def send_message(msg):
    ws.send(msg)

ws = None
chk_cancel = False

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:9001",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

