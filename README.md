# CloakRoom

Welcome to **CloakRoom** – your ultimate solution for secure application messaging. CloakRoom allows you to establish a robust connection that ensures the confidentiality, authentication, and integrity of your messages between clients and servers, all implemented using the Python programming language.

## Key Features

CloakRoom provides the following key features to guarantee a secure communication channel:

- **Message Confidentiality:** All messages from the client to the server are confidential, assuming trust in the security of public keys.

- **Message Integrity:** The server should verify that the received message has remained intact all the way it traveled from the client.

## Running the code

To run the specific version of the encrypted messaging, you'll need to run the files from their respective sub-directories.

i.e.: `./ASYMMETRIC_ONLY` or `./ASYMMETRIC_SYMMETRIC`

First, start the server: `python -u server.py`

To receive a message from the server, the command is as follows:

`python -u client.py recv_msg`

To send a message to the server, the command is as follows:

`python -u client.py send_msg "message_to_send"`

You are also able to generate new RSA key pair on either the client or server by issuing the `generate_key_pair` command.

`python -u client.py generate_key_pair`

`python -u server.py generate_key_pair`
