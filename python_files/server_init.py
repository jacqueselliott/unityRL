from websocket_server import WebsocketServer
import sys
#https://github.com/Pithikos/python-websocket-server/blob/master/websocket_server/websocket_server.py

simul_id = 0
deep_id = 0
# Called for every client connecting (after handshake)
def proc_new_client(client, server):
	print("New client connected and was given id %d" % client['id'])


# Called for every client disconnecting
def proc_client_left(client, server):
	print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def proc_message_received(client, server, message):
	if len(message) > 200:
		message = message[:200]+'..'
	print("Client(%d) said: %s" % (client['id'], message))


PORT=9001
server = WebsocketServer(PORT)

def start_server():
	server.set_fn_new_client(proc_new_client)
	server.set_fn_client_left(proc_client_left)
	server.set_fn_message_received(proc_message_received)
	server.run_forever()

if __name__ == "__main__":
    start_server()