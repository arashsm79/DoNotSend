import unittest
from donotsend.converter import *

class TestConverter(unittest.TestCase):

    def test_b32encode_1(self):
        self.assertEqual(b32encode("test"), "ORSXG5A")
        self.assertNotEqual(b32encode("test"), "ORSXG5A=")

    def test_b32encode_2(self):
        self.assertEqual(b32encode("asdlkfjhasdkjfhkefhKJHDaskdjha1293487AsdjJhas@!#%"), "MFZWI3DLMZVGQYLTMRVWUZTINNSWM2CLJJEEIYLTNNSGU2DBGEZDSMZUHA3UC43ENJFGQYLTIAQSGJI")
        self.assertNotEqual(b32encode("asdlkfjhasdkjfhkefhKJHDaskdjha1293487AsdjJhas@!#%"), "MFZWI3DLMZVGQYLTMRVWUZTINNSWM2CLJJEEIYLTNNSGU2DBGEZDSMZUHA3UC43ENJFGQYLTIAQSGJI=")

    def test_b32decode_1(self):
        self.assertEqual(b32decode("MFZWI3DLMZVGQYLTMRVWUZTINNSWM2CLJJEEIYLTNNSGU2DBGEZDSMZUHA3UC43ENJFGQYLTIAQSGJI"), "asdlkfjhasdkjfhkefhKJHDaskdjha1293487AsdjJhas@!#%")

    def test_b32decode_2(self):
        self.assertEqual(b32decode("ORSXG5A"), "test")
        self.assertEqual(b32decode("ORSXG5A="), "test")

    def test_1_b64encode(self):
        self.assertEqual(b64encode("test"), "dGVzdA")

    def test_2_b64encode(self):
        self.assertEqual(b64encode("Ali"), "QWxp")

    def test_3_b64encode(self):
        self.assertEqual(b64encode("Hasan"), "SGFzYW4")

    def test_4_b64encode(self):
        with self.assertRaises(TypeError):
            self.assertEqual(b64encode(512), "BGEvYZ9")

    def test_1_b64decode(self):
        self.assertEqual(b64decode("dGVzdA=="), "test")

    def test_2_b64decode(self):
        self.assertEqual(b64decode("QWxp"), "Ali")

    def test_3_b64decode(self):
        self.assertEqual(b64decode("SGFzYW4="), "Hasan")

    def test_4_b64decode(self):
        with self.assertRaises(TypeError):
            self.assertEqual(b64decode(354.45), "Reza")
