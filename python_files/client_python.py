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
    global data_received, data_message
    if data_received == False:
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
    q_network_simple_sim.main(ws)

def send_message(msg, ws_in = None):
    if ws_in is None:
        ws.send(msg)
    else:
        ws_in.send(msg)

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

