from model_client import Client
import time


connectedClients = {}
# TODO hanlde locking


def findClient(clientId: str) -> Client:
    if clientId not in connectedClients.keys():
        return Client(clientId, None)
    return connectedClients[clientId][0]


def pushClient(client: Client):
    connectedClients[client.id] = (client, time.time())


def popClient(client: Client):
    connectedClients.pop(client.id)


def listConnected():
    return connectedClients.keys()


def isConnectedClient(client: Client):
    if client.id in connectedClients.keys():
        return True
    else:
        return False
