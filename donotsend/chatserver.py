#!/usr/bin/env python3

from datetime import datetime
import secrets
import time
from typing import List, Union

from donotsend.server import main


MESSAGE_LIMIT = 10000
USER_LIMIT = 1000
MAX_MESSAGES_AT_ONCE = 25

ERROR_UNKNOWN_USERTAG = """ERROR The given usertag is unknown to the system.|
Please request a new one from the system with:|
|
/register word"""
ERROR_NOT_REGISTERED = """ERROR You're not identified.|
You need to request a usertag with '/register tag',|
then identify when sending commands and messages with:|
@usertag message here"""
ERROR_TOO_MANY_USERS = """ERROR Too many users are currently logged in.|
This mecanism exists to prevent the demo server from|
out of memory errors.|
Please try again later."""


class Message:
    def __init__(self, author: str, content: str):
        self.author = author
        self.content = content
        self.timestamp = time.time()

    def __str__(self):
        d = datetime.fromtimestamp(self.timestamp).strftime("%d/%m %H:%M:%S")
        return f"@{self.author} [{d}] -- {self.content}"


class User:
    def __init__(self, name: str, ip: str, suffix: Union[int, str] = ""):
        self.tag = name
        self.suffix = suffix
        self.ip = ip
        self.created_at = time.time()

    @property
    def name(self):
        return f"{self.tag}{self.suffix}"

    @staticmethod
    def generate_usertag(word: str) -> str:
        return f"{word}{secrets.randbits(8 * 2)}"


class ChatServer:
    def __init__(self):
        self.messages = []
        self.users = {}  # usertag: User

    def register_user(self, content: List[str], ip: str) -> Union[str, bool]:
        if USER_LIMIT > 0 and len(self.users) < USER_LIMIT:
            word, *_ = content
            already_existing = len(
                [u for u in self.users.values() if u.tag == word]
            )
            user = User(word, ip, already_existing or "")
            usertag = User.generate_usertag(user.name)
            self.users[usertag] = user
            return f"Registered as {usertag}."
        return False  # avoid having too many users for now

    def consult(self, args: List[str]) -> str:
        # no arguments
        count = 5
        from_user = ""

        if len(args) > 0:
            try:
                count = int(args[0])
                count = min(MAX_MESSAGES_AT_ONCE, max(0, count))
            except ValueError:
                pass
            from_user = args[1] if len(args) > 1 else from_user

        i, out = 0, []
        for msg in self.messages[::-1]:
            if not from_user or msg.author == from_user:
                out.append(str(msg))

            if i == count:
                break
            i += 1

        return "|".join(out)

    def check_command(self, msg: str, ip: str) -> str:
        msg = msg.strip()

        if msg.startswith("/"):
            cmd, *data = msg.split(" ")
            if cmd == "/register":
                result = self.register_user(data, ip)
                if not result:
                    return ERROR_TOO_MANY_USERS
                return result
            elif cmd == "/consult":
                return self.consult(data)
            else:
                return "ERROR Unknown command."
        elif msg.startswith("@"):
            if len(self.messages) >= MESSAGE_LIMIT:
                self.messages = self.messages[-int(MESSAGE_LIMIT / 1000 + 1) :]

            usertag, *data = msg.split(" ")
            # remove the @
            usertag = usertag[1:]
            if usertag not in self.users:
                return ERROR_UNKNOWN_USERTAG
            else:
                self.messages.append(Message(self.users[usertag].name, " ".join(data)))
                return "OK."
        else:
            return ERROR_NOT_REGISTERED

    def __call__(self, message: str, src_ip: str, domains: List[str]) -> str:
        return self.check_command(message, src_ip)


if __name__ == "__main__":
    main(chat=ChatServer())
