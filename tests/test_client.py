import unittest
from donotsend.client import *
from donotsend.server import main
import os
from threading import Thread
import time
import sys

class TestClient(unittest.TestCase):
    
    t1 = Thread()
    def startServer():
    	os.system("python3 donotsend/chatserver.py tests/configs/test_config.ini")
    
    @classmethod
    def setUpClass(cls):
        cls.logger = init_logger()
        cls.t1 = Thread(target=cls.startServer)
        cls.t1.start()
        time.sleep(2)
    
    def test_1_send(self):
        client = Client("chat.localhost", get_ip_from_hostname("chat.localhost"))
        self.assertIn("DNS",client.send("Hello"))

    def test_2_send(self):
        client = Client("chat.localhos", get_ip_from_hostname("chat.localhost"))
        with self.assertRaises(AttributeError):
            client.send("Hello")
            
    def test_1_recv(self):
        client = Client("chat.localhost", get_ip_from_hostname("chat.localhost"))
        pkt = client.send("Hello")
        with self.assertRaises(AttributeError) as cm:
            client.recv(pkt)
        self.assertIn("info",cm.exception.args[0])

    def test_2_recv(self):
        client = Client("chat.localhost", get_ip_from_hostname("chat.localhost"))
        with self.assertRaises(AttributeError) as cm:
            client.recv(None)
        self.assertIn("warning",cm.exception.args[0])
        
    def test_1_main(self):
        fileCompletePath = sys.argv[0]
        sys.argv = [fileCompletePath]
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, -1)
        
    def test_2_main(self):
        fileCompletePath = sys.argv[0]
        sys.argv = [fileCompletePath, 'localst:53']
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, -1)
        
    def test_3_main(self):
        fileCompletePath = sys.argv[0]
        sys.argv = [fileCompletePath, 'localhost']
        with self.assertRaises(AttributeError) as cm:
            main()
        self.assertIn("info",cm.exception.args[0])
        
    def test_4_main(self):
        fileCompletePath = sys.argv[0]
        sys.argv = [fileCompletePath, 'localhost:53', "gqgqeg", "fqwffa"]
        with self.assertRaises(AttributeError) as cm:
            main()
        self.assertIn("info",cm.exception.args[0])

    #def test_5_main(self):
    #    fileCompletePath = sys.argv[0]
    #    sys.argv = [fileCompletePath, 'localht']
    #    with self.assertRaises(SystemExit) as cm:
    #        main()
    #    self.assertEqual(cm.exception.code, -1)
        
    #def test_6_main(self):
    #    fileCompletePath = sys.argv[0]
    #    sys.argv = [fileCompletePath, 'localhost:53']
    #    with self.assertRaises(AttributeError) as cm:
    #        main()
    #    self.assertIn("info",cm.exception.args[0])
        
    #def test_7_main(self):
    #    fileCompletePath = sys.argv[0]
    #    sys.argv = [fileCompletePath, 'localhost', "gdsgsdg"]
    #    with self.assertRaises(AttributeError) as cm:
    #        main()
    #    self.assertIn("info",cm.exception.args[0])
if __name__ == '__main__':
    unittest.main()

