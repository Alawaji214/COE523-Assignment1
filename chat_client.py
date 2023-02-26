import socket
import logging
import time

from message import Message

'''
@Quit
Syntax: @Quit
Purpose: user types it at the client prompt to end his session
'''
def quit():
    raise NotImplementedError

'''
@List
Syntax: @List
Purpose: user types it at the client prompt to view the current list of online clients
'''
def list():
    raise NotImplementedError

'''
General Message to some other client
Syntax: (otherclientid) message-statement
Purpose: typed by the user at the client prompt when he want to send a message to an online
client
'''
def send_message():
    raise NotImplementedError


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
    logging.warning("Start Clinet")
    # loopback address (internal calls)
    HOST = "127.0.0.1" 
    TCP_PORT = 9992 
    
    message = "msg"

    # TODO: connect
    # TODO: Read input (client ID) < 8 bytes

    # TODO: send connect (receive the length of the regular intervals - in response to the connect message)

# TODO: parallel
    # TODO: auto send regular alive based on regular intervals
    # TODO: listen to updated list
    # TODO: input from user
        # TODO: command handling (quit, list)
        # TODO: send messages to otherclients (other client id, message)
    # TODO: recive messages from otherclients (message)


    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # client.sendto(str.encode(message),(HOST,TCP_PORT))
    # client.bind((HOST,TCP_PORT))
    client.connect((HOST,TCP_PORT))

    src = "A"
    dest = "-SERVER-"
    connect = "Connect"
    list = "List"
    quit = "Quit"
    # ser = "B".ljust(8) + src.ljust(8) + content + '\0'
    cona_mes = Message("A",dest,connect)
    conb_mes = Message("B",dest,connect)
    conc_mes = Message("C",dest,connect)
    list_mes = Message(src,dest,list)
    quit_mes = Message(src,dest,quit)

    client.send(cona_mes.serialize().encode())
    time.sleep(2)
    client.send(conb_mes.serialize().encode())
    time.sleep(1)
    client.send(list_mes.serialize().encode())

    # client.send(conb_mes.serialize().encode())
    # client.send(conc_mes.serialize().encode())
    time.sleep(20)
    logging.warning("End Clinet")

if __name__ == '__main__':
    main()
