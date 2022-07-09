import random
import string
from scapy.error import Scapy_Exception
from donotsend.utils import DNSAnswer
from scapy.layers.dns import DNSRR, DNS, dnstypes
from scapy.layers.inet import IP, UDP

import unittest
from donotsend.packet import *
from donotsend.converter import *
from donotsend.utils import DNSHeaders


class TestPacket(unittest.TestCase):
    def test_build_tos(self):
        ret = build_tos(0, 0, 0, 0, 0)
        self.assertEqual(ret, 0)

        ret = build_tos(0, 0, 1, 1, 1)
        self.assertEqual(ret, 14)

        ret = build_tos(0, 0, 0, 0, 1)
        self.assertEqual(ret, 2)

        ret = build_tos(0, 0, 0, 1, 0)
        self.assertEqual(ret, 4)

        ret = build_tos(0, 0, 1, 0, 0)
        self.assertEqual(ret, 8)

        ret = build_tos(0, 1, 0, 1, 0)
        self.assertEqual(ret, 20)

        ret = build_tos(0, 1, 0, 0, 1)
        self.assertEqual(ret, 18)

        ret = build_tos(0, 1, 1, 0, 0)
        self.assertEqual(ret, 24)

    def test_build_query_1(self):
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
        self.assertTrue(packet._pkt.haslayer(IP))
        self.assertEqual(packet._pkt[IP].src, ip)
        self.assertEqual(packet._pkt[IP].dst, ip)
        self.assertEqual(packet._pkt[IP].proto, 17)

        self.assertTrue(packet._pkt.haslayer(UDP))
        self.assertEqual(packet._pkt[UDP].dport, port)
        self.assertTrue(packet._pkt.haslayer(DNS))

        self.assertTrue(packet._pkt[DNS].qd.qname.decode('ASCII').endswith(domain))
        self.assertEqual(packet._pkt[DNS].qd.qtype, 16)

    def test_build_query_2(self):
        message = "Hello"
        domain = "localhost"
        ip = "invalid"
        port = 53
        crafted_domain = f"{Domain.encode(message)}.{domain}"
        with self.assertRaises(OSError) as cm:
            packet = Packet.build_query(
                {
                    "dst": ip,
                    "dport": port,
                    "dns": {"qname": crafted_domain},
                },
                domain,
            )
        self.assertIsInstance(cm.exception, OSError)

    def test_build_reply_1(self):
        domain = "localhost"
        ip = "127.0.0.1"
        port = 53
        pktid = 12
        question  = "test_question"
        data = "test_data"
        qname = "test_qname"
        ttl = 60
        packet = Packet.build_reply(
                {
                    "src": ip,
                    "dst": ip,
                    "sport": port,
                    "dport": port,
                    "dns": {
                        "id": pktid,
                        "question": question,
                        "messages": [
                                DNSRR(
                                    rrname=qname,
                                    rdata=data,
                                    type=DNSAnswer.Type.Text,
                                    ttl=ttl,
                                ),
                            ],
                        },
                    },
                domain,
                )
        self.assertTrue(packet._pkt.haslayer(IP))
        self.assertEqual(packet._pkt[IP].src, ip)
        self.assertEqual(packet._pkt[IP].dst, ip)
        self.assertEqual(packet._pkt[IP].proto, 17)

        self.assertTrue(packet._pkt.haslayer(UDP))
        self.assertEqual(packet._pkt[UDP].dport, port)
        self.assertEqual(packet._pkt[UDP].sport, port)

        self.assertTrue(packet._pkt.haslayer(DNS))
        self.assertEqual(packet._pkt[DNS].id, pktid)
        self.assertEqual(packet._pkt[DNS].qd.decode('ASCII'), question)
        self.assertEqual(packet._pkt[DNS].an.rrname.decode('ASCII'), qname)
        self.assertEqual(packet._pkt[DNS].an.rdata[0], data)
        self.assertEqual(packet._pkt[DNS].an.ttl, ttl)
        self.assertEqual(packet._pkt[DNS].an.type, 16)

    def test_build_reply_2(self):
        domain = "localhost"
        ip = "invalid"
        port = 53
        pktid = 12
        question  = "test_question"
        data = "test_data"
        qname = "test_qname"
        ttl = 60
        with self.assertRaises(OSError) as cm:
            packet = Packet.build_reply(
                    {
                        "src": ip,
                        "dst": ip,
                        "sport": port,
                        "dport": port,
                        "dns": {
                            "id": pktid,
                            "question": question,
                            "messages": [
                                    DNSRR(
                                        rrname=qname,
                                        rdata=data,
                                        type=DNSAnswer.Type.Text,
                                        ttl=ttl,
                                    ),
                                ],
                            },
                        },
                    domain,
                    )
        self.assertIsInstance(cm.exception, OSError)

    def test_answers(self):
        domain = "localhost"
        ip = "127.0.0.1"
        port = 53
        pktid = 12
        question  = "test_question"
        data = b'test_data'
        qname = b'test_qnameaksjdhaksjdh'
        ttl = 60
        packet = Packet.build_reply(
                {
                    "src": ip,
                    "dst": ip,
                    "sport": port,
                    "dport": port,
                    "dns": {
                        "id": pktid,
                        "question": question,
                        "messages": [
                                DNSRR(
                                    rrname=qname,
                                    rdata=data,
                                    type=DNSAnswer.Type.Text,
                                    ttl=ttl,
                                ),
                            ],
                        },
                    },
                domain,
                )
        self.assertEqual(packet.answers[0][1], data.decode('utf-8'))
        self.assertEqual(packet.answers[0][0], qname.decode('utf-8'))
