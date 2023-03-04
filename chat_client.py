import socket
import logging
import time
import sys
# import str
import threading

from common import Message, bcolors
from queue import Queue
from _thread import *

import common

SERVER_ID = "-SERVER-"
CONNECT = "Connect"
LIST = "List"
QUIT = "Quit"
ALIVE = "Alive"


class Client:
    def __init__(self, id: str, socket: socket.socket):
        if len(id) > 8:
            logging.error("Invalid id of client, {id}", id)
            raise ValueError
        # Add ' ' padding until its length eqauls 8 bytes
        self.id: str = id.ljust(8)
        self.socket = socket
        self.send_queue = Queue()

    '''
    Connect
    Syntax: Connect clientid
    Purpose: automatically sent by a client to the server when the client comes online
    '''

    def connect(self):
        logging.info("%s wants to connect", self.id)

        resps = self.send_request_with_resp(
            Message(self.id, SERVER_ID, CONNECT)).split(b'\0')

        logging.info("timeout : %s", resps[0].decode())
        self.timeout = int(Message.deserialize(resps.pop(0)).content)

        # Handle the case where more than one message is queued
        for resp in resps:
            if not resp:
                continue
            print(Message.deserialize(resp).content)

        print(self.timeout)
        start_new_thread(self.alive, ())
        start_new_thread(self.connection_handler, ())
        start_new_thread(self.connection_listener, ())

    '''
    Alive
    Syntax: Alive clientid
    Purpose: automatically sent by client to server after regular intervals that it is still alive
    '''

    def alive(self):
        while self.timeout:
            self.send_queue.put(Message(self.id, SERVER_ID, ALIVE))
            time.sleep(self.timeout)

    '''
    @Quit
    Syntax: @Quit
    Purpose: user types it at the client prompt to end his session
    '''

    def quit(self):
        logging.info("%s wants to quit", self.id)
        self.send_request(Message(self.id, SERVER_ID, QUIT))
        self.timeout = 0

    '''
    @List
    Syntax: @List
    Purpose: user types it at the client prompt to view the current list of online clients
    '''

    def list(self):
        logging.info("%s wants list of connected clients", self.id)
        self.send_queue.put(Message(self.id, SERVER_ID, LIST))

    '''
    General Message to some other client
    Syntax: (otherclientid) message-statement
    Purpose: typed by the user at the client prompt when he want to send a message to an online
    client
    '''

    def send_message(self, args):

        if len(args) < 2:
            raise ValueError

        other_client = args[0]
        content = args[1]
        self.send_queue.put(Message(self.id, other_client, content))

    def send_request_with_resp(self, message: Message):
        self.socket.send(message.serialize().encode())
        resp = self.socket.recv(256)
        return resp

    def send_request(self, message: Message):
        self.socket.send(message.serialize().encode())

    def connection_listener(self):
        logging.info("started connection listener")

        while self.timeout:
            resp = self.socket.recv(256)
            if resp:
                msg = Message.deserialize(resp)

                match msg.src:
                    case b'-SERVER-':
                        print("new message from %s: %s" %
                              (msg.src.decode(), msg.content.decode()))
                    case _:
                        print("new message from %s: %s" %
                              (msg.src.decode(), msg.content.decode()))

    def connection_handler(self):
        logging.info("started connection handler")

        while self.timeout:
            msg = self.send_queue.get()
            logging.info("sending %s", msg.serialize())
            self.send_request(msg)

        logging.info("Ending connection handler")
        self.socket.close()

    def interactive_handler(self):
        logging.info("%s  is in the interactive handler", self.id)
        print("You are now logged on")

        while self.timeout:
            promt = input(
                f"{bcolors.OKBLUE}Enter your command : {bcolors.ENDC}")
            if not promt:
                continue

            cmd = promt.split(" ", 1)
            match cmd[0]:
                case "@Quit":
                    self.quit()
                case "@List":
                    self.list()
                case _:
                    self.send_message(cmd)


def select_clientID():
    client_id = input("Enter your client ID : ")
    print(client_id)

    while not common.isValidClientID(client_id):
        logging.warning("Invalid client id was entered")
        client_id = input("Invalid ID, select another one : ")

    return client_id


'''
chatclient:
On startup, each client will connect to the server and sends its id provided by the user. The server
will register this client. Each client is required to send an alive message to the server after regular
intervals so that the server is updated about its presence. The server will tell to the client about
the length of this interval in response to the connect message. If the server doesn’t receive an
alive message from some client then it de-lists it and sends the latest list to all online clients.
Whenever a client wants to send a message, it sends a message to the server with the target
clientid. Clients can also request the latest client list by sending a message to server.
'''


def main():
    logging.info("Start Clinet")
    # loopback address (internal calls)
    HOST = "127.0.0.1"
    TCP_PORT = 9992

    message = "msg"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, TCP_PORT))
        print("You are now connected")
        logging.info("You are now connected")
        clientID = select_clientID()

        client = Client(clientID, client)
        client.connect()#CONNECT COMMAND SENT
        client.interactive_handler()

    except socket.error:
        print("Failed to connect")
        logging.error("Failed to connect")

    logging.warning("End Clinet")


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    main()
