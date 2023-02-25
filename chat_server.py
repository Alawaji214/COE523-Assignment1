# import socket programming library
import socket
import socketserver
import deprecation

# import thread module
from _thread import *
import threading
import logging

'''
HOST = "localhost"
TCP_PORT = 9992 
'''

@deprecation
class TCPMessageHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        name = self.request[0].strip()
        socket = self.request[1]
        print(name,"wrote:".format(self.client_address[0]))
        print(data)
        socket.sendto(data.upper(), self.client_address)

@deprecation
def socketserver_main():
    HOST = "localhost"
    UDP_PORT = 9991 
    TCP_PORT = 9992
    
    udp_server = socketserver.UDPServer((HOST, UDP_PORT), UDPMessageHandler)
    tcp_server = socketserver.TCPServer((HOST, TCP_PORT), TCPMessageHandler)
    udp_server.serve_forever()
    tcp_server.serve_forever()

'''
Connect
Syntax: Connect clientid
Purpose: automatically sent by a client to the server when the client comes online
'''
def connect():
	raise NotImplementedError

'''
Quit
Syntax: Quit clientid
Purpose: automatically sent by a client to the server when a user requests for session end
'''
def quit():
	# TODO: send list to all connected clients
	raise NotImplementedError

'''
List
Syntax: List
Purpose: automatically sent by a client to the server when a user requests the list of online clients
'''
def list():
    raise NotImplementedError

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
'''
# thread function
def message_handler(c):
	while True:

		# data received from client
		data = c.recv(1024)
		if not data:
			logging.warning('Bye')			
			break

		# reverse the given string from client
		data = data[::-1]

		# send back reversed string to client
		c.send(data)

	# connection closed
	c.close()

def socket_main():
	logging.info("Started ChatServer")
	
	host = ""

	# reserve a port on your computer
	# in our case it is 12345 but it
	# can be anything
	port = 12345
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	logging.info("socket binded to port", port)

	# put the socket into listening mode
	s.listen(5)
	logging.info("socket is listening")

	# a forever loop until client wants to exit
	while True:

		# establish connection with client
		c, addr = s.accept()

		logging.info('Connected to :', addr[0], ':', addr[1])

		# Start a new thread and return its identifier
		start_new_thread(message_handler, (c,))
	s.close()


if __name__ == '__main__':
	socket_main()
