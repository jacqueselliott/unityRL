from __future__ import division
import websocket
import threading
from random import randint
import sys
import q_network_simple_sim

queue_received = []
count = 0

def on_message(ws, message):
    queue_received.append(message)
    send_message(str(randint(0,3)))
    # if int(x) < 4 and int(x) > -1:
    #     print(str(x))
    #     send_message(str(x))

def on_error(ws, error):
    print(error)

def on_close(ws):
    pass

def on_open(ws):
    send_message('client')

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

