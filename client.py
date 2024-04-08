import socket
import threading
import sys
import encryption

if len(sys.argv) != 3:
    print("Usage: ./client.py <IP> <PORT>")
    exit()

HOST = str(sys.argv[1])
PORT = int(sys.argv[2])

if PORT < 0 or PORT > 65535 or not isinstance(PORT, int):
    print("Port number must be between 0 and 65535")
    exit()

client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def send():
    username = input("Enter your username: ")
    client.send(username.encode('utf-8'))
    while True:
        message = input('')
        if message.startswith('/file_encrypt'):
            file_path = message.split()[1]
            encryption.encrypt_file("password123", file_path, "encrypted_file.enc")
            with open("encrypted_file.enc", "rb") as f:
                data = f.read(1024)
                while data:
                    client.send(data)
                    data = f.read(1024)
            print("File encrypted and sent.")
        else:
            client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()
