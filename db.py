from model_client import Client
from typing import NamedTuple
import time


connectedClients = {}
# TODO hanlde locking


def findClient(clientId: str) -> Client:
    return connectedClients[clientId][0]


def pushClient(client: Client):
    connectedClients[client.id] = (client, time.time())


def popClient(client: Client):
    connectedClients.pop(client.id)


def listConnected():
    return connectedClients.keys()


def isConnectedClient(client: Client):
    if client.id in connectedClients.keys:
        return True
    else:
        return False
