import socket
import threading
import os

# Define the list of authorized users
authorized_users = {
    "userA": "UbuntuChatKey_A",
    "userB": "UbuntuChatKey_B",
    "ubuntu": "UbuntuChatKey"  # This is the admin user
}

# Define the port and server address
HOST = '0.0.0.0'  # Bind to all available network interfaces
PORT = 12345      # Choose a suitable port number

# Create a socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

# Maintain a list of connected clients
connected_clients = []

# Function to process incoming messages
def handle_client(client_socket, client_address):
    username = None

    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            if not username:
                # If the user is not logged in, validate their identity
                if data in authorized_users:
                    username = data
                    client_socket.send("Login successful. You are now logged in.".encode())
                    connected_clients.append((client_socket, username))
                else:
                    client_socket.send("Invalid username. Connection closed.".encode())
                    break
            elif username == "ubuntu":
                # Admin options
                if data == "a":
                    client_socket.send("You are in chat mode.".encode())
                    while True:
                        chat_message = client_socket.recv(1024).decode()
                        if chat_message:
                            log_message(username, chat_message)
                            broadcast_message(username, chat_message)
                elif data == "b":
                    client_socket.send("You are in AWS terminal mode.".encode())
                    # Implement code to allow admin to enter the AWS terminal
                else:
                    client_socket.send("Invalid option.".encode())
            else:
                log_message(username, data)
                broadcast_message(username, data)

        except Exception as e:
            print(f"Error: {str(e)}")
            break

# Function to log messages
def log_message(username, message):
    with open("ChatLogs.txt", "a") as log_file:
        log_file.write(f"{username}: {message}\n")

# Function to broadcast messages to connected clients
def broadcast_message(sender, message):
    for client, username in connected_clients:
        if username != "ubuntu" or sender != "ubuntu":
            try:
                client.send(f"{sender}: {message}".encode())
            except Exception as e:
                print(f"Error broadcasting message to {username}: {str(e)}")

# Main loop to accept incoming connections
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()
