# import socket programming library
import socket
import threading
import logging
# import custom class Message
from model_message import Message
# import thread module
from _thread import *
from routes import *
import socket as socketModule
from socket import socket

HOST = "localhost"
TCP_PORT = 9992
TIMEOUT_INTERVAL = 5
MAX_CLIENT = 5
SERVER_ID = b'-SERVER-'


def message_handler(data, srcSocket: socket):
    logging.info("message_handler")
    msg = Message.deserialize(data)
    msg.src.socket = srcSocket
    
    logging.info("msg %s-%s-%s", msg.dest.id, msg.src.id, msg.content)

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


def client_handler(c: socket):
    getpeername = c.getpeername()
    while True:
        payload = c.recv(256)
        # TODO if payload has Quit, Or No need for below
        if not payload:
            logging.warning('Empty message')
            break
        logging.info("getpeername %s payload %s", getpeername, payload)
        message_handler(payload, c)
    logging.info("Bye %s", getpeername)
    c.close()


def prepareSocket() -> socket:
    s = socketModule.socket(socketModule.AF_INET, socketModule.SOCK_STREAM)
    s.bind((HOST, TCP_PORT))
    logging.info("socket binded to port %s", TCP_PORT)
    # put the socket into listening mode
    s.listen(MAX_CLIENT)
    logging.info("socket is listening")
    return s


def socket_main():
    logging.basicConfig(level='INFO')
    logging.info("Started ChatServer")
    s = prepareSocket()
    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        try:
            c, addr = s.accept()
            logging.info('Connected to : %s:%s', addr[0], addr[1])
            # Start a new thread and return its identifier
            # TODO use pool instead
            start_new_thread(client_handler, (c,))
        except socketModule.error:
            logging.error("Error in establishing connection")
    # NEVER REACHED
    s.close()


if __name__ == '__main__':
    socket_main()
