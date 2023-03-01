# import socket programming library
import socket
import threading
import logging

# import custom class Message
from model_message import Message
# import thread module
from _thread import *
# import Queue data structure
from routes import *

HOST = "localhost"
TCP_PORT = 9992
TIMEOUT_INTERVAL = 5
MAX_CLIENT = 5
SERVER_ID = b'-SERVER-'


def message_handler(data):
    logging.info("message_handler")
    msg = Message.deserialize(data)
    logging.info("msg %s-%s-%s", msg.dest, msg.src, msg.content)

    if msg.dest == SERVER_ID:
        logging.info("content %s", msg.content)
        match msg.content:
            case b'Connect':
                connect(msg.src)
            case b'List':
                list()
            case b'Quit':
                quit(msg.src)
            case b'Alive':
                alive(msg.src)
            case _:
                logging.warning("unidentified content %s", msg.content)

    else:
        general_message(msg)

    # raise NotImplementedError


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
    # c.settimeout(TIMEOUT_INTERVAL)
    client = c.getpeername()
    while True:
        # TODO: client handler should be aware of the client
        # data received from client
        # try:
        data = c.recv(256)
        if not data:
            logging.warning('Empty message')
            break
        logging.info("%s sent %s", client, data)
        message_handler(data)
        # except socket.timeout:
        # 	logging.warning("%s timeout", client)
        # 	#quit
        # 	break;

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
            # use pool instead
            start_new_thread(client_handler, (c,))

        except socket.error:
            logging.error("Error in establishing connection")

    s.close()


if __name__ == '__main__':
    socket_main()
