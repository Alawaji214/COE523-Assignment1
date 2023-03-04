# import socket programming library
import socket
import threading
import logging
import time
from datetime import datetime
# import custom class Message
from common import Message
# import thread module
from _thread import *
# import Queue data structure
from queue import Queue

HOST = "localhost"
TCP_PORT = 9992
TIMEOUT_INTERVAL = 11
MAX_CLIENT = 5
SERVER_ID = "-SERVER-"
TIMEOUT_BUFFER = 1

online_list = {}
online_list_lock = threading.Lock()

message_db = Queue()

'''
Connect
Syntax: Connect clientid
Purpose: automatically sent by a client to the server when the client comes online
'''


def connect(client, socket):
    logging.info("%s wants to connect", client)
    # lock online list
    with online_list_lock:
        if client in online_list:
            logging.info("%s is already connected", client)
            raise ValueError

        online_list[client] = (socket, datetime.now())
        logging.info("%s connected", client)
        message_db.put(Message(SERVER_ID, client,
                       str(TIMEOUT_INTERVAL).ljust(8)))

    list_to_all()


'''
Quit
Syntax: Quit clientid
Purpose: automatically sent by a client to the server when a user requests for session end
'''


def quit(client):
    logging.info("%s quit", client)
    with online_list_lock:
        try:
            online_list.pop(client)
        except KeyError:
            logging.warning("%s not found", client)

    list_to_all()


'''
List
Syntax: List
Purpose: automatically sent by a client to the server when a user requests the list of online clients
'''


def list(client):
    logging.info("%s list", client)
    list_of_clients = "".join(online_list.keys())[:239]
    message_db.put(Message(SERVER_ID, client, list_of_clients))


'''
Send an updated list to all connected clients 
'''


def list_to_all():
    logging.info("list_to_all")

    with online_list_lock:
        connected_clients = online_list.keys()
        list_of_clients = "List of connected clients: " + \
            "".join(connected_clients)[:239]

    for client in connected_clients:
        message_db.put(Message(SERVER_ID, client, list_of_clients))


'''
Alive
Syntax: Alive clientid
Purpose: automatically sent by client to server after regular intervals that it is still alive
'''


def alive(client):
    logging.info("%s alive", client)
    # the connection will not be closed if it is active
    # the timeout is in watch by connection.settimeout(TIMEOUT_INTERVAL + TIMEOUT_BUFFER) from connection_handler


'''
checkAlive
Syntax: Alive clientid
Purpose: automatically sent by client to server after regular intervals that it is still alive
'''

def checkAlive():
    now = datetime.now()
    with online_list_lock:
        for clientId, client in online_list.items():
            delta = now - client[1]
            if delta.seconds > TIMEOUT_INTERVAL:
                logging.info("checkAlive - online_list.pop(clientId) %s", clientId)
                online_list.pop(clientId)
    logging.info("updating alive list")
    time.sleep(TIMEOUT_INTERVAL)
    checkAlive()

'''
General Message to some other client
Syntax: (otherclientid) message-statement
Purpose: typed by the user at the client prompt when he want to send a message to an online
client
'''


def general_message(msg):
    logging.info("general_message")

    if msg.dest.decode() in online_list:
        message_db.put(
            Message(msg.src.decode(), msg.dest.decode(), msg.content.decode()))
    else:
        message_db.put(Message(SERVER_ID, msg.src.decode(),
                       "the target client is not online"))


def message_handler(data):
    logging.info("message_handler")
    msg = Message.deserialize(data)
    logging.info("msg %s-%s-%s", msg.dest, msg.src, msg.content)

    src = msg.src.decode()
    dest = msg.dest.decode()
    content = msg.content.decode()

    if msg.dest.decode() == SERVER_ID:
        logging.info("content %s", msg.content)
        match content:
            case "List":
                list(src)
            case "Quit":
                quit(src)
            case "Alive":
                alive(src)
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
connection_handler --> client_handler --> message_handler --> Action
'''


def connection_handler(connection):
    connection.settimeout(TIMEOUT_INTERVAL + TIMEOUT_BUFFER)
    client_addr = connection.getpeername()

    data = connection.recv(256)
    if data:
        msg = Message.deserialize(data)
        client_id = msg.src.decode()

        if msg.content == b'Connect':
            logging.info("%s wants to connect as (%s)", client_addr, client_id)
            connect(client_id, connection)

            # start handling client
            client_handler(connection, msg.src)
        else:
            logging.info("%s sent invalid request (%s)",
                         client_addr, msg.content)

    # connection closed
    close_connection(connection)

# clients sender thread function


def clients_sender():
    # TODO:
    while True:
        try:
            msg = message_db.get()
            dest = msg.dest
            connection = online_list[dest][0]
            connection.send(msg.serialize().encode())
        except Exception as e:
            logging.error("failed to send due to %s", error)


# client listener thread function
def client_handler(connection, client):
    logging.info("client %s logged in", client)

    while True:
        try:
            data = connection.recv(256)
            if not data:
                logging.warning('Empty message')
                break
            logging.info("%s sent %s", client, data)
            message_handler(data)
        except socket.timeout:
            logging.warning("%s timeout", client)
            quit(client)
            break


def close_connection(connection):
    logging.info("closing %s", connection.getpeername())
    connection.close()


def socket_main():
    logging.info("Started ChatServer")

    # to check alive list
    start_new_thread(checkAlive, ())

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, TCP_PORT))
    logging.info("socket binded to port %s", TCP_PORT)

    # put the socket into listening mode
    s.listen(MAX_CLIENT)
    logging.info("socket is listening")

    # start a thread for sending messages for all clients
    start_new_thread(clients_sender, ())

    # a forever loop until client wants to exit
    while True:

        # establish connection with client
        try:
            c, addr = s.accept()
            logging.info('Connected to : %s:%s', addr[0], addr[1])
            # Start a new thread and return its identifier
            start_new_thread(connection_handler, (c,))

        except socket.error:
            logging.error("Error in establishing connection")
            break

    s.close()
    logging.info("ChatServer End")


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    socket_main()
