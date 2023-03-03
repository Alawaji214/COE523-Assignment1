import logging
from model_client import Client
from model_message import Message
import db
import pickle
'''
Connect
Syntax: Connect clientid
Purpose: automatically sent by a client to the server when the client comes online
'''


def connect(client: Client):
    logging.info("%s wants to connect", client)
    db.pushClient(client=client)
    logging.info("%s connected", client)
    sendLatestList()


'''
Quit
Syntax: Quit clientid
Purpose: automatically sent by a client to the server when a user requests for session end
'''


def quit(client: Client):
    logging.info("%s quit", client)
    db.popClient(client=client)
    sendLatestList()


'''
List
Syntax: List
Purpose: automatically sent by a client to the server when a user requests the list of online clients
'''


def list():
    return db.listConnected()


'''
Alive
Syntax: Alive clientid
Purpose: automatically sent by client to server after regular intervals that it is still alive
'''


def alive(client: Client):
    db.pushClient(client=client)


'''
General Message to some other client
Syntax: (otherclientid) message-statement
Purpose: typed by the user at the client prompt when he want to send a message to an online
client
'''


def general_message(msg: Message, src: Client, dest: Client):
    if db.isConnectedClient(dest.id) and dest.socket is not None:
        dest.socket.send(msg.content.encode())
    else:
        src.socket.send("client is not online".encode())


def sendLatestList():
    connected = db.listConnected()
    for client in db.connectedClientsList():
        c = Client(client[0].id, client[0].socket)
        c.socket.send(pickle.dumps(connected))
        # recd = pickle.loads(msg)