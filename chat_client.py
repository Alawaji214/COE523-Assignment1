import socket
import logging

def main():
    logging.warning("Start Clinet")
    HOST = "127.0.0.1"
    UDP_PORT = 9991 
    TCP_PORT = 9992
    
    udp_server = (HOST,UDP_PORT)

    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    client.sendto(str.encode("Hi"),(HOST,UDP_PORT))

    logging.warning("End Clinet")


if __name__ == '__main__':
    main()
