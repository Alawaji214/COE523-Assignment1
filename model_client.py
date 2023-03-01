import logging
from socket import socket

class Client:
    def __init__(self, id: str, socket: socket):
        if len(id) > 8:
            logging.error("Invalid id of client, {id}", id)
            raise ValueError
        # Add ' ' padding until its length eqauls 8 bytes
        self.id: str = id.ljust(8)
        self.socket = socket
        
    def __eq__(self, other): 
        if not isinstance(other, Client):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.id == other.id
