# Unit tests for DoNotSend
> This repo contains unit tests for [DoNotSend](https://github.com/SuperFola/DoNotSend): Sending messages by hacking the DNS protocol. 

* [test_chatserver.py](#test-chatserver)
* [test_client.py](#test-client)
* [test_converter.py](#test-converter)
* [test_packet.py](#test-packet)
* [test_server.py](#test-server)

# test chatserver
|function name|test method|
|---|---|
|register_user | Modified condition/decision coverage|
|consult | Edge-pair coverage|
|check_command|Prime path coverage|

# test client
|function name|test method|
|---|---|
|send | Prime path coverage|
|recv | Decision coverage|
|main | Decision coverage|

# test converter
|function name|test method|
|---|---|
|b32encode | Special Value Testing|
|b32decode | Special Value Testing|
|b64encode | Equivalence class|
|b64decode | Special Value Testing|

# test packet
|function name|test method|
|---|---|
|build_tos | Orthogonal array|
|build_query | Equivalence class|
|build_reply  | Equivalence class|
|answers | Special Value Testing|

# test server
|function name|test method|
|---|---|
|_make_a | Special Value Testing|
|_make_txt| Special Value Testing|
|from_file  | Equivalence class|
|main| Prime path coverage|
|_dns_responder|Equivalence class|


---
These tests were written in collaboration with [MohammadMohammadZadehKalati](https://github.com/MohammadMohammadZadehKalati).
