import unittest
from donotsend.client import *
import os
from threading import Thread
import time

class TestClient(unittest.TestCase):
    
    def startServer():
    	os.system("python3 donotsend/chatserver.py tests/configs/test_config2.ini")
    
    @classmethod
    def setUpClass(cls):
        t1 = Thread(target=cls.startServer)
        t1.start()
        time.sleep(2)
    
    def test_2_send(self):
        client = Client("chat.localhost", get_ip_from_hostname("chat.localhost"), 2727)
        self.assertIn("DNS",client.send("Hello"))

    def test_4_send(self):
        client = Client("chat.localhost", get_ip_from_hostname("chat.localhost"), 2728)
        with self.assertRaises(AttributeError):
            self.assertIn("DNS",client.send("Hello"))

if __name__ == '__main__':
    unittest.main()

