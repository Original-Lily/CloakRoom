# CloakRoom

Welcome to **CloakRoom** – my solution for secure application messaging. CloakRoom allows you to establish a robust connection that ensures the confidentiality, authentication, and integrity of your messages between clients and servers, all implemented using the Python programming language, utilizing socket programming and threading. 

A server is set up, allowing multiple clients to establish a connection to a server and the server broadcast the messages that clients send to each other. This project also has an logging and command-execution features. Clients can run specific commands such as number of online users or clearing the chat. And, All the messages ,that are sent by clients, are logged by the server in a server.log file.

## Key Features

• All messages from client to the server are confidential, through AES algorithm

• Command-line tools enable meta-data on the current session to be explored

• Client-Server architecture allowing multiple clients to connect and commune

• Multithreading is implemented to handle simultaneous sending & recieving of messages

• Reliable packet communication via TCP

## Running the code

To run the encrypted messaging, you'll need to first ensure the required python modules are installed on your device:

```pip install -r requirements.txt```

To start the server: ```./server.py <hostIP> <port>```

In order to join the server as a client: ```./client.py <hostIP> <port>```

Upon successful connection:

```Welcome! ```
```Enter your username: ```

While in the chat room, you can use commands such as:

```/count``` to return the number of users currently online

```/users``` to return a list of users in your session

```/clear``` to clear away all text on screen

```/help``` to display your command options
