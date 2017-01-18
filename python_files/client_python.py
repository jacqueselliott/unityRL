from __future__ import division
from websocket import create_connection
import sys
import q_network_simple_sim
import time

def send_message_sync(msg, ws):
    ws.send(msg)
    result = None
    while result is None:
        result =  ws.recv()
    return result
    
def main(argv):
    ws = create_connection("ws://localhost:9001")
    ws.send('client')
    q_network_simple_sim.main(ws)

if __name__ == "__main__":
    main(sys.argv)


