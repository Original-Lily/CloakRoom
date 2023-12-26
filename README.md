# CloakRoom

Welcome to **CloakRoom** – your ultimate solution for secure application messaging. CloakRoom allows you to establish a robust connection that ensures the confidentiality, authentication, and integrity of your messages between clients and servers, all implemented using the Python programming language.

This process is similar to components that exist in many applications (e.g. secure email, SSH, ..). The secure connection should provide:

• Message confidentiality

• Sender authentication

• Message integrity

• and symmetric key distribution


## Key Features

• All messages from client to the server are confidential. It is assumed both ends trust the public keys

• Message security is ensured, meaning it cannot be read even if intercepted

• Server verifies message integrity between clients

• The client generates a secret key and uses a symmetric algorithm to encrypt the message and signature

• The client uses the server’s public key to encrypt the secret key


## Running the code

To run the encrypted messaging, you'll need to first ensure the required python modules are installed on your device:

`pip install -r requirements.txt`

To start the server: `python -u server.py`

To receive a message from the server, the command is as follows:

`python -u client.py recv_msg`

To send a message to the server:

`python -u client.py send_msg "example message"`

You are also able to generate new RSA key pair on either the client or server by issuing the `generate_key_pair` command

`python -u client.py generate_key_pair`

`python -u server.py generate_key_pair`

