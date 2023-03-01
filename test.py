import unittest

from model_message import Message
import chat_server as cs
import chat_client as cc
from model_client import Client
from socket import socket
from db import connectedClients
class TestStringMethods(unittest.TestCase):

    def test_valid_message(self):
        src = Client("A", socket=None)
        dest =  Client("B", socket=None)
        content = "Hi B, I am A"
        ser = dest.id.ljust(8) + src.id.ljust(8) + content + '\0'

        mes = Message(src,dest,content)
        self.assertEqual(Message.serialize(mes),ser)
        
    def test_invalid_dest(self):
        src = Client("A", socket=None)
        dest = Client("C", socket=None)
        content = "Hi B, I am A"
        ser = "B".ljust(8) + src.id.ljust(8) + content + '\0'

        mes = Message(src,dest,content)
        self.assertNotEqual(Message.serialize(mes),ser)

    def test_large_content(self):
        src = Client("A", socket=None)
        dest = Client("B", socket=None)
        content = "012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"

        with self.assertRaises(ValueError):
            mes = Message(src,dest,content)

    def test_deserilize(self):
        src = Client("A", socket=None)
        dest = Client("B", socket=None)
        cs.connect(src)
        cs.connect(dest)
        content = "Hi B, I am A"
        ser = dest.id.ljust(8) + src.id.ljust(8) + content + '\0'

        mes = Message(src,dest,content)
        mes2 = Message.deserialize(ser)

        self.assertEqual(mes.src,mes2.src)
        self.assertEqual(mes.dest,mes2.dest)
        self.assertEqual(mes.content,mes2.content)
        cs.quit(src)
        cs.quit(dest)

    def test_connect(self):
        a: Client = Client("A", socket=None)
        b: Client = Client("B", socket=None)
        cs.connect(a)
        cs.connect(b)
        connect = cs.list()
        self.assertEqual(len(connect), 2)
        cs.quit(a)
        cs.quit(b)

    def test_quit(self):
        c: Client = Client("C", socket=None)
        d: Client = Client("D", socket=None)
        cs.connect(c)
        cs.connect(d)
        connect = cs.list()
        self.assertEqual(len(connect), 2)
        cs.quit(d)
        connect = cs.list()
        self.assertEqual(len(connect), 1) 
        cs.quit(c)
        connect = cs.list()
        self.assertEqual(len(connect), 0) 
                         
if __name__ == '__main__':
    unittest.main()