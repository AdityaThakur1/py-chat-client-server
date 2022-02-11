import socket
import threading

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 12341
ADDRESS = (SERVER, PORT)


# all the clients connected to the server
clients, cli_names = [], []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

#connection start
def startServer():

	print("The current IP of the server is: " + SERVER)
	server.listen()
	
	while True:
		connection, addr = server.accept()
		connection.send("NAME".encode("utf-8"))
		
		name = connection.recv(1024).decode("utf-8")
		
		cli_names.append(name)
		clients.append(connection)
		
		print(f"The name of new client is :{name}")
		
		# broadcast message
		broadcastMessage(f"{name} has joined!".encode("utf-8"))
		
		connection.send('Connection to the chat server successful!'.encode("utf-8"))
		
		# Start the handling thread
		thread = threading.Thread(target = handle, args = (connection, addr))
		thread.start()
		
		print(f"Total number of active connections {threading.activeCount()-1}")

def handle(connection, addr):

	print(f"The new connection added is {addr}")
	connected = True
	
	while connected:
		message = connection.recv(1024)
		broadcastMessage(message)
	connection.close()

def broadcastMessage(message):
	for client in clients:
		client.send(message)

# call the method to start the chat server
startServer()
