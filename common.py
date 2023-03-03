import logging
# import str

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def isValidClientID(client_id: str):
    return len(client_id) <= 8

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
    def __init__(self, src, dest, content):
        if not isValidClientID(src):
            logging.error("Invalid source")
            raise ValueError

        if not isValidClientID(dest):
            logging.error("Invalid destination")
            raise ValueError

        if not len(content) <= 239:
            logging.error("Invalid content")
            raise ValueError

        # Add ' ' padding until its length eqauls 8 bytes
        self.src = src.ljust(8)
        self.dest = dest.ljust(8)
        self.content = content

    '''
Return raw message
        # First 8 bytes are the name of destination
        # next 8 bytes are the name of the source
        # content
        # null termination

    '''
    def serialize(self):
        message = "".join([self.dest,self.src,self.content,'\0'])
        return message
  
    '''
Take raw message and return Message instance
    '''
    def deserialize(message: str):
        # 8 + 8 + 1 = 17, src length + dest length + null termination
        if len(message) > 256 or len(message) < 17:
            logging.error("Invalid message")
            raise ValueError

        destination = message[0:8]
        source      = message[8:16]
        content      = message[16:-1]
        return Message(source,destination,content)
