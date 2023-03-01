import logging
from model_client import Client
from db import findClient
'''
A message sent by a process (client/server) to another. It is a null terminated string with the
maximum length of 255 bytes (256th byte is null). First 8 bytes are the name of destination, next
8 bytes are the name of the source and the remaining bytes up-to the null byte are the actual
message. It means that the actual message length can’t be more than 239 bytes. It also implies
that a client name can’t be more than 8 bytes, and if some client has name less than 8 bytes then
you have to perform padding to keep it of 8 Bytes. Moreover, as the server sends the list of online
clients through a message and the message length is limited, therefore, either you have to limit
the number of concurrent clients or use some other way to send the list in more than one
iterations.
'''
class Message:
    def __init__(self, src: Client, dest: Client, content: str):
        # checking id of client don on Client object
        if len(content) > 239:
            logging.error("Invalid content")
            raise ValueError
        self.src = src
        self.dest = dest
        self.content = content

    '''
Return raw message
        # First 8 bytes are the name of destination
        # next 8 bytes are the name of the source
        # content
        # null termination
    '''
    def serialize(self):
        message = "".join([self.dest.id,self.src.id,self.content,'\0'])
        return message
  
    '''
Take raw message and return Message instance
    '''
    def deserialize(message):
        # 8 + 8 + 1 = 17, src length + dest length + null termination
        if len(message) > 256 or len(message) < 17:
            logging.error("Invalid message")
            raise ValueError
        destination = findClient(message[0:8])
        source = findClient(message[8:16])
        content      = message[16:-1]
        return Message(source,destination,content)
