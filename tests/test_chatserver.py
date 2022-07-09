import random
import string

import unittest
from donotsend.chatserver import *


class TestChatServer(unittest.TestCase):
    def test_message(self):
        author = "".join(
            random.choice(string.ascii_lowercase) for i in range(random.randint(10, 50))
        )
        content = "".join(
            random.choice(string.ascii_lowercase) for i in range(random.randint(10, 50))
        )
        msg = Message(author=author, content=content)
        self.assertTrue(str(msg).startswith("@" + author))
        self.assertTrue(str(msg).endswith(content))

    def test_register_user_1(self):
        import donotsend.chatserver as cs
        old_user_limit = cs.USER_LIMIT
        cs.USER_LIMIT = 1
        chat_server = cs.ChatServer()
        self.assertEqual(len(chat_server.users), 0)
        ret = chat_server.register_user(["testuserA"], "127.0.0.1")
        self.assertTrue(str(ret).startswith("Registered as testuserA"))
        self.assertEqual(len(chat_server.users), 1)

        ret = chat_server.register_user(["testuserB"], "127.0.0.1")
        self.assertFalse(ret)
        cs.USER_LIMIT = old_user_limit

    def test_register_user_2(self):
        import donotsend.chatserver as cs
        old_user_limit = cs.USER_LIMIT
        cs.USER_LIMIT = -1
        chat_server = cs.ChatServer()
        self.assertEqual(len(chat_server.users), 0)
        ret = chat_server.register_user(["testuser"], "127.0.0.1")
        self.assertFalse(ret)
        self.assertEqual(len(chat_server.users), 0)
        cs.USER_LIMIT = old_user_limit

    def test_register_user_3(self):
        import donotsend.chatserver as cs
        chat_server = cs.ChatServer()
        self.assertEqual(len(chat_server.users), 0)
        ret = chat_server.register_user(["testuser"], "127.0.0.1")
        self.assertTrue(str(ret).startswith("Registered as testuser"))

    def test_register_user_4(self):
        import donotsend.chatserver as cs
        chat_server = cs.ChatServer()
        self.assertEqual(len(chat_server.users), 0)
        ret = chat_server.register_user(["testuserA"], "127.0.0.1")
        self.assertTrue(str(ret).startswith("Registered as testuserA"))
        self.assertEqual(len(chat_server.users), 1)
        usertag = ret.split(" ")[-1].split(".")[0]
        self.assertEqual(chat_server.users[usertag].suffix, '')

        ret = chat_server.register_user(["testuserA"], "127.0.0.1")
        usertag = ret.split(" ")[-1].split(".")[0]
        self.assertTrue(str(ret).startswith("Registered as testuserA"))
        self.assertEqual(chat_server.users[usertag].suffix, 1)
        self.assertTrue(chat_server.users[usertag].name.startswith("testuserA1"))

    def test_register_user_5(self):
        import donotsend.chatserver as cs
        chat_server = cs.ChatServer()
        self.assertEqual(len(chat_server.users), 0)
        ret = chat_server.register_user(["testuserA"], "127.0.0.1")
        self.assertTrue(str(ret).startswith("Registered as testuserA"))
        self.assertEqual(len(chat_server.users), 1)
        usertag = ret.split(" ")[-1].split(".")[0]
        self.assertEqual(chat_server.users[usertag].suffix, '')

        ret = chat_server.register_user(["testuserA"], "127.0.0.1")
        usertag = ret.split(" ")[-1].split(".")[0]
        self.assertTrue(str(ret).startswith("Registered as testuserA"))
        self.assertEqual(chat_server.users[usertag].suffix, 1)
        self.assertTrue(chat_server.users[usertag].name.startswith("testuserA1"))

        ret = chat_server.register_user(["testuserA"], "127.0.0.1")
        usertag = ret.split(" ")[-1].split(".")[0]
        self.assertTrue(str(ret).startswith("Registered as testuserA"))
        self.assertEqual(chat_server.users[usertag].suffix, 2)
        self.assertTrue(chat_server.users[usertag].name.startswith("testuserA2"))

    def test_consult_1(self):
        chat_server = ChatServer()
        chat_server.messages.append(Message("Arash","Hello"))
        chat_server.messages.append(Message("Arash2","Hi!"))
        ret = chat_server.consult(["5", "nonexistentuser"])
        self.assertEqual(ret, "")

    def test_consult_2(self):
        chat_server = ChatServer()
        chat_server.messages.append(Message("Arash2","Hi!"))
        chat_server.messages.append(Message("Arash","Hello"))
        ret = chat_server.consult(["1", "Arash"])
        self.assertTrue(ret.startswith("@Arash") and ret.endswith("Hello"))

    def test_consult_3(self):
        chat_server = ChatServer()
        ret = chat_server.consult([])
        self.assertEqual(ret, "")

    def test_consult_4(self):
        chat_server = ChatServer()
        chat_server.messages.append(Message("Arash","Hello"))
        ret = chat_server.consult(["0", "Arash"])
        self.assertTrue(ret.startswith("@Arash") and ret.endswith("Hello"))

    def test_consult_5(self):
        chat_server = ChatServer()
        chat_server.messages.append(Message("Arash","Hello"))
        ret = chat_server.consult(["5", "nonexistentuser"])
        self.assertEqual(ret, "")

    def test_consult_6(self):
        chat_server = ChatServer()
        chat_server.messages.append(Message("Arash","Hello"))
        chat_server.messages.append(Message("Arash2","Hello"))
        chat_server.messages.append(Message("Arash3","Hello"))
        chat_server.messages.append(Message("Arash4","Hello"))
        ret = chat_server.consult(["2"])
        self.assertTrue(len(ret.split("|")), 3)


    def test_1_check_command(self):
        chatserver = ChatServer()
        counter = 0
        usertags = []
        for i in range(1000):
            tempResult = chatserver.check_command("/register test","127.0.0.1")
            if tempResult != ERROR_TOO_MANY_USERS:
                usertags.append(tempResult)
                counter = counter + 1
        for element in usertags:
            if usertags.count(element) > 1:
                print(usertags)
                self.assertTrue(usertags.count(element) == 1, "Repeated usertag: " + element.split(" ")[-1][:-1] + " was found!")
        self.assertTrue(True)

    def test_2_check_command(self):
        self.assertIn("Registered as test", ChatServer.check_command(ChatServer(),"/register test","127.0.0.1"))

    def test_3_check_command(self):
        self.assertEqual(ChatServer.check_command(ChatServer(),"/consult 5","127.0.0.1"), "")

    def test_4_check_command(self):
        chatserver = ChatServer()
        chatserver.messages.append(Message("Ali","Hello"))
        chatserver.messages.append(Message("Ali","Hi!"))
        self.assertIn("Hi!", chatserver.check_command("/consult 5","127.0.0.1"))

    def test_5_check_command(self):
        self.assertEqual(ChatServer.check_command(ChatServer(),"/confirm Ali","127.0.0.1"), "ERROR Unknown command.")

    def test_6_check_command(self):
        self.assertEqual(ChatServer.check_command(ChatServer(),"@Hasan Hi!","127.0.0.1"), ERROR_UNKNOWN_USERTAG)

    def test_7_check_command(self):
        chatserver = ChatServer()
        UserTag = chatserver.check_command("/register Hasan","127.0.0.1").split(" ")[-1][:-1]
        self.assertEqual(chatserver.check_command("@" + UserTag + " test","127.0.0.1"), "OK.")

    def test_8_check_command(self):
        chatserver = ChatServer()
        chatserver.messages = [Message("Reza", "test")]*10000
        chatserver.check_command("@Hossein test","127.0.0.1")
        self.assertEqual(len(chatserver.messages),11)

    def test_9_check_command(self):
        chatserver = ChatServer()
        chatserver.messages = [Message("Reza", "test")]*10000
        UserTag = chatserver.check_command("/register Hossein","127.0.0.1").split(" ")[-1][:-1]
        chatserver.check_command("@" + UserTag + " message","127.0.0.1")
        self.assertEqual(chatserver.messages[-1].content, "message")

    def test_10_check_command(self):
        self.assertEqual(ChatServer.check_command(ChatServer(),"test","127.0.0.1"), ERROR_NOT_REGISTERED)

