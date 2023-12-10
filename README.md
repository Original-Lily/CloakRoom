# CloakRoom

Welcome to **CloakRoom** – your ultimate solution for secure application messaging. CloakRoom allows you to establish a robust connection that ensures the confidentiality, authentication, and integrity of your messages between clients and servers, all implemented using the Python programming language.

## Key Features

CloakRoom provides the following key features to guarantee a secure communication channel:

- **Message Confidentiality:** All messages from the client to the server are confidential, assuming trust in the security of public keys.

- **Sender Authentication:** Utilize a verification diagram to allow the server to verify that it is receiving the message from the client and not anyone else.

- **Message Integrity:** The server should verify that the received message has remained intact all the way it traveled from the client.

- **Symmetric Key Distribution:** Efficient symmetric key distribution for encrypting and decrypting messages securely.

## Implementation

### Part 1

In this phase, CloakRoom encrypts messages using an asymmetric key for enhanced security. Key aspects of Part 1 include:

- Encrypting messages with the server's public key to ensure confidentiality.

- Utilizing a verification diagram for server authentication.

- Verifying the integrity of the received message.

- Demonstrating message confidentiality, even in case of interception during transit.

### Part 2

Building upon Part 1, CloakRoom optimizes the process for larger messages. Key features in Part 2 include:

- Generating a secret key on the client side for symmetric encryption.

- Employing a symmetric algorithm to encrypt both the message and its signature.

- Encrypting the secret key with the server's public key.

- Sending the combined output to the server.

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