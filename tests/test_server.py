import unittest
from donotsend.server import *
from donotsend.packet import *
from donotsend.client import *
from donotsend.converter import *
import os
from threading import Thread
import time
import sys
from scapy.sendrecv import sr1
from scapy.error import Scapy_Exception


class TestServer2(unittest.TestCase):
    def test_make_a(self):
        sv = Server.from_file("tests/configs/test_config.ini")
        domain = "localhost"
        message = "Hello"
        ip = "127.0.0.1"
        port = 53
        crafted_domain = "example.com."
        reqpkt = Packet.build_query(
            {
                "dst": ip,
                "dport": port,
                "dns": {"qname": crafted_domain},
            },
            domain,
        )

        packet = sv._make_a(reqpkt)
        self.assertTrue(packet._pkt.haslayer(IP))
        self.assertEqual(packet._pkt[IP].src, ip)
        self.assertEqual(packet._pkt[IP].dst, ip)
        self.assertEqual(packet._pkt[IP].proto, 17)

        self.assertTrue(packet._pkt.haslayer(UDP))
        self.assertEqual(packet._pkt[UDP].sport, 9090)

        self.assertTrue(packet._pkt.haslayer(DNS))
        self.assertEqual(packet._pkt[DNS].an.rrname.decode('ASCII'), crafted_domain)
        self.assertEqual(packet._pkt[DNS].an.rdata, "122.122.122.1")
        self.assertEqual(packet._pkt[DNS].an.ttl, 3600)
        self.assertEqual(packet._pkt[DNS].an.type, 1)

    def test_make_txt(self):
        sv = Server.from_file("tests/configs/test_config.ini")

        domain = "localhost"
        message = "Hello"
        ip = "127.0.0.1"
        port = 53
        crafted_domain = b32encode("testdom") + ".localhost.com"
        reqpkt = Packet.build_query(
            {
                "dst": ip,
                "dport": port,
                "dns": {"qname": crafted_domain},
            },
            domain,
        )

        packet = sv._make_txt(reqpkt)
        self.assertTrue(packet._pkt.haslayer(IP))
        self.assertEqual(packet._pkt[IP].src, ip)
        self.assertEqual(packet._pkt[IP].dst, ip)
        self.assertEqual(packet._pkt[IP].proto, 17)

        self.assertTrue(packet._pkt.haslayer(UDP))
        self.assertEqual(packet._pkt[UDP].sport, 9090)

        self.assertTrue(packet._pkt.haslayer(DNS))
        self.assertEqual(packet._pkt[DNS].an.rrname.decode('ASCII'), crafted_domain)
        self.assertEqual(packet._pkt[DNS].an.rdata[0], b64encode("test"))
        self.assertEqual(packet._pkt[DNS].an.ttl, 1)
        self.assertEqual(packet._pkt[DNS].an.type, 16)

    def test_make_message(self):
        sv = Server.from_file("tests/configs/test_config.ini")
        qname = "testqname"
        content = "testcontent"
        msg = sv._make_message(qname,content)
        self.assertEqual(msg.rrname.decode('utf-8'), qname)
        self.assertEqual(msg.rdata[0], b64encode(content))



class TestServer(unittest.TestCase):

    t1 = Thread()

    def startServer():
        os.system("sudo python3 chatserver.py tests/configs/test_config.ini")

    @classmethod
    def setUpClass(cls):
        cls.logger = init_logger()
        cls.t1 = Thread(target=cls.startServer)
        cls.t1.start()
        time.sleep(2)

    def test_1_main(self):
        fileCompletePath = sys.argv[0]
        sys.argv = [fileCompletePath]
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, -1)

    def test_2_main(self):
        fileCompletePath = sys.argv[0]
        sys.argv = [
            fileCompletePath,
            "tests/configs/test_config.ini",
        ]
        with self.assertRaises(FileNotFoundError):
            main()

    def test_3_main(self):
        fileCompletePath = sys.argv[0]
        sys.argv = [fileCompletePath, "tests/configs/test_config.ini", "loc"]
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, -1)

    def test_4_main(self):
        fileCompletePath = sys.argv[0]
        sys.argv = [fileCompletePath, "tests/configs/test_config.ini", 523]
        with self.assertRaises(TypeError):
            main()

    def test_5_main(self):
        fileCompletePath = sys.argv[0]
        sys.argv = [fileCompletePath, "tests/configs/test_config.ini", "localhost"]
        with self.assertRaises(Scapy_Exception) as cm:
            main()
        self.assertIsInstance(cm.exception, Scapy_Exception)

    def test_1_dns_responder(self):
        message = "Hello"
        domain = "localhost"
        ip = "127.0.0.1"
        port = 53
        crafted_domain = f"{Domain.encode(message)}.{domain}"

        packet = Packet.build_query(
            {
                "dst": ip,
                "dport": port,
                "dns": {"qname": crafted_domain},
            },
            domain,
        )
        answer = sr1(packet.packet, verbose=2, timeout=1)

    def test_2_dns_responder(self):
        message = "Hello"
        domain = "localhst"
        ip = "127.0.0.1"
        port = 53
        crafted_domain = f"{Domain.encode(message)}.{domain}"

        packet = Packet.build_query(
            {
                "dst": ip,
                "dport": port,
                "dns": {"qname": crafted_domain},
            },
            domain,
        )
        answer = sr1(packet.packet, verbose=2, timeout=1)

    def test_3_dns_responder(self):
        message = "Hello"
        domain = "localhost"
        ip = "127.0.0.0"
        port = 53
        crafted_domain = f"{Domain.encode(message)}.{domain}"

        packet = Packet.build_query(
            {
                "dst": ip,
                "dport": port,
                "dns": {"qname": crafted_domain},
            },
            domain,
        )
        answer = sr1(packet.packet, verbose=2, timeout=1)

    def test_4_dns_responder(self):
        message = "Hello"
        domain = "localhost"
        ip = "127.0.0.2"
        port = 53
        crafted_domain = f"{Domain.encode(message)}.{domain}"

        packet = Packet.build_query(
            {
                "dst": ip,
                "dport": port,
                "dns": {"qname": crafted_domain},
            },
            domain,
        )
        answer = sr1(packet.packet, verbose=2, timeout=1)

    def test_5_dns_responder(self):
        message = "Hello"
        domain = "localhost"
        ip = "127.0.0.1"
        port = 0
        crafted_domain = f"{Domain.encode(message)}.{domain}"

        packet = Packet.build_query(
            {
                "dst": ip,
                "dport": port,
                "dns": {"qname": crafted_domain},
            },
            domain,
        )
        answer = sr1(packet.packet, verbose=2, timeout=1)


if __name__ == "__main__":
    unittest.main()
