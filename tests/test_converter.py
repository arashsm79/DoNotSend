import unittest
from donotsend.converter import *

class TestConverter(unittest.TestCase):

    def test_b32encode(self):
        self.assertEqual(b32encode("test"), "ORSXG5A")
        self.assertNotEqual(b32encode("test"), "ORSXG5A=")

    def test_b32decode(self):
        self.assertEqual(b32decode("ORSXG5A"), "test")
