# import socket programming library
import socket
import threading
import logging

# import custom class Message
from message import Message
# import thread module
from _thread import *
# import Queue data structure
from queue import Queue

HOST = "localhost"
TCP_PORT = 9992 
TIMEOUT_INTERVAL = 5
MAX_CLIENT = 5

online_list = {}
online_list_lock = threading.Lock()

class Client:
    def __init__(self, id):
        self.id = id
        self.msg_db = Queue()

'''
Connect
Syntax: Connect clientid
Purpose: automatically sent by a client to the server when the client comes online
'''
def connect(client):
	# lock online list
	with online_list_lock:
		logging.info("%s connected", client)
		online_list[client] = Queue()

'''
Quit
Syntax: Quit clientid
Purpose: automatically sent by a client to the server when a user requests for session end
'''
def quit(client):
	with online_list_lock:
		logging.info("%s quit", client)
		try:
			online_list.pop(client)
		except KeyError:
			logging.warning("%s not found", client)

	# TODO: send list to all connected clients

'''
List
Syntax: List
Purpose: automatically sent by a client to the server when a user requests the list of online clients
'''
def list():
    return online_list.keys()

'''
Alive
Syntax: Alive clientid
Purpose: automatically sent by client to server after regular intervals that it is still alive
'''
def alive():
    raise NotImplementedError

'''
General Message to some other client
Syntax: (otherclientid) message-statement
Purpose: typed by the user at the client prompt when he want to send a message to an online
client
'''
def general_message():
	raise NotImplementedError


def message_handler():

	# alive
	# connect
	# list
	# 

	raise NotImplementedError

'''
chatserver:
On startup, server will create a socket to receive client connections and messages. One client can
send a message to another client via the server. All messaging is done through the server. It
means that whenever a client has to send a message to another client; it will send the message
with the target clientid to the server to be forwarded to another client. Clients can also send
messages to the server to get some information in response. The server if it receives a message
for a client, who is not online anymore, respond to the source client with a message that the target
client is not online. The server will keep a list of online clients with it and clients can ask about
this list by sending a message to the server. The server is also responsible for sending the latest
client list to all the clients whenever there is a change in it.

Client lifecycle
TCPConnection --(connect)--> Connected --(quit)--> Offline
'''
# thread function
def client_handler(c):
	c.settimeout(TIMEOUT_INTERVAL)
	client = c.getpeername()
	while True:
		
		# data received from client
		try:
			data = c.recv(1024)
			if not data:
				logging.warning('Empty message')			
				break
			logging.info("%s sent %s", client, data)

		except socket.timeout:
			logging.warning("%s timeout", client)
			#quit
			break; 

	logging.info("Bye %s", client)			
	# connection closed
	c.close()

def socket_main():
	logging.basicConfig(level='INFO')
	logging.info("Started ChatServer")
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, TCP_PORT))
	logging.info("socket binded to port %s", TCP_PORT)

	# put the socket into listening mode
	s.listen(MAX_CLIENT)
	logging.info("socket is listening")
	
	# a forever loop until client wants to exit
	while True:

		# establish connection with client
		try:
			c, addr = s.accept()
			logging.info('Connected to : %s:%s', addr[0], addr[1])
			# Start a new thread and return its identifier
			start_new_thread(client_handler, (c,))

		except socket.error:
			logging.error("Error in establishing connection")

	s.close()


if __name__ == '__main__':
	socket_main()
