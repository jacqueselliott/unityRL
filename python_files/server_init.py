from websocket_server import WebsocketServer

#https://github.com/Pithikos/python-websocket-server/blob/master/websocket_server/websocket_server.py
PORT=9001
server = WebsocketServer(PORT)
simul_id = {}
deep_id = {}

# Called for every client connecting (after handshake)
def proc_new_client(client, server):
	pass


# Called for every client disconnecting
def proc_client_left(client, server):
	global simul_id, deep_id
	if 'id' in simul_id:
		if simul_id['id'] == client['id']:
			simul_id = {}
	if 'id' in deep_id:
		if deep_id['id'] == client['id']:
			deep_id = {}

# Called when a client sends a message
def proc_message_received(client, server, message):
	global simul_id, deep_id
	if message == 'client':
		deep_id = client
		print('Client connected!')
	elif message == 'unity':
		simul_id = client
		print('Unity agent connected!')
	else:
		#Parse message id
		if 'id' in simul_id and 'id' in deep_id:
			if client['id'] == simul_id['id']:
				#Send to client
				server.send_message(deep_id, message)
			elif client['id'] == deep_id['id']:
				#Send to simulation
				server.send_message(simul_id, message)

def start_server():
	global simul_id, deep_id
	server.set_fn_new_client(proc_new_client)
	server.set_fn_client_left(proc_client_left)
	server.set_fn_message_received(proc_message_received)
	server.run_forever()

if __name__ == "__main__":
    start_server()