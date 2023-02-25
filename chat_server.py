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
UDP_PORT = 9991 
TCP_PORT = 9992 
'''

class UDPMessageHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        name = self.request[0].strip()
        socket = self.request[1]
        print(name,"wrote:".format(self.client_address[0]))
        print(data)
        socket.sendto(data.upper(), self.client_address)

class TCPMessageHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        name = self.request[0].strip()
        socket = self.request[1]
        print(name,"wrote:".format(self.client_address[0]))
        print(data)
        socket.sendto(data.upper(), self.client_address)

def socketserver_main():
    HOST = "localhost"
    UDP_PORT = 9991 
    TCP_PORT = 9992
    
    udp_server = socketserver.UDPServer((HOST, UDP_PORT), UDPMessageHandler)
    tcp_server = socketserver.TCPServer((HOST, TCP_PORT), TCPMessageHandler)
    udp_server.serve_forever()
    tcp_server.serve_forever()


# thread function
@deprecation
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

@deprecation
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
	socketserver_main()
