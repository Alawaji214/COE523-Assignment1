import unittest

from message import Message

class TestStringMethods(unittest.TestCase):

    def test_valid_message(self):
        src = "A"
        dest = "B"
        content = "Hi B, I am A"
        ser = dest.ljust(8) + src.ljust(8) + content + '\0'

        mes = Message(src,dest,content)
        self.assertEqual(Message.serialize(mes),ser)
        
    def test_invalid_dest(self):
        src = "A"
        dest = "C"
        content = "Hi B, I am A"
        ser = "B".ljust(8) + src.ljust(8) + content + '\0'

        mes = Message(src,dest,content)
        self.assertNotEqual(Message.serialize(mes),ser)

    def test_large_content(self):
        src = "A"
        dest = "B"
        content = "012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"

        with self.assertRaises(ValueError):
            mes = Message(src,dest,content)

    def test_deserilize(self):
        src = "A"
        dest = "B"
        content = "Hi B, I am A"
        ser = dest.ljust(8) + src.ljust(8) + content + '\0'

        mes = Message(src,dest,content)
        mes2 = Message.deserialize(ser)

        self.assertEqual(mes.src,mes2.src)
        self.assertEqual(mes.dest,mes2.dest)
        self.assertEqual(mes.content,mes2.content)

if __name__ == '__main__':
    unittest.main()