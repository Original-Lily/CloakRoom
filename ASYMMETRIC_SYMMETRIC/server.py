from cryptography.fernet import Fernet
import rsa
import socket
import sys


def gen_key_pair():
    SERVER_PUB_KEY, SERVER_PRV_KEY = rsa.newkeys(2048)
    
    with open("server_public.pem", "wb") as f:
        f.write(SERVER_PUB_KEY.save_pkcs1("PEM"))

    with open("server_private.pem", "wb") as f:
        f.write(SERVER_PRV_KEY.save_pkcs1("PEM"))

    SERVER_PUB_KEY = None
    SERVER_PRV_KEY = None

    sys.exit()


def send_message(c_socket, msg):
    symmetric_key = Fernet.generate_key()

    with open("server_private.pem", "rb") as f:
        SERVER_PRV_KEY = rsa.PrivateKey.load_pkcs1(f.read())
    hash_digest_signature = rsa.sign(msg.encode("utf-8"), SERVER_PRV_KEY, "SHA-256")

    with open("client_public.pem", "rb") as f:
        CLIENT_PUB_KEY = rsa.PublicKey.load_pkcs1(f.read())
    data_block = [list(hash_digest_signature), msg]
    
    encr_data_block = Fernet(symmetric_key).encrypt(bytes(str(data_block).encode("utf-8")))
    encr_symmetric_key = rsa.encrypt(symmetric_key, CLIENT_PUB_KEY)

    c_socket.send(encr_symmetric_key)
    c_socket.recv(1024)
    c_socket.send(encr_data_block)
    c_socket.recv(1024)

    print("\nIntercepting the data block while in transit would look like this:")
    print(encr_data_block)
    print("\nIntercepting the symmetric key while in transit would look like this:")
    print(hash_digest_signature)


def receive_message(c_socket):
    encr_symmetric_key = c_socket.recv(10240)
    c_socket.send(bytes(f"Received symmetric key", "utf-8"))
    encr_data_block = c_socket.recv(10240)
    c_socket.send(bytes(f"Received data block", "utf-8"))

    try:
        with open("server_private.pem", "rb") as f:
            SERVER_PRV_KEY = rsa.PrivateKey.load_pkcs1(f.read())
        decr_symmetric_key = rsa.decrypt(encr_symmetric_key, SERVER_PRV_KEY)

        decr_data_block = Fernet(decr_symmetric_key).decrypt(encr_data_block).decode("utf-8")
        hash_digest_signature = bytes([int(i) for i in decr_data_block[2:decr_data_block.find("], '")].split(", ")])
        msg = decr_data_block[decr_data_block.find("], '") + 4:-2]
    except:
        print("Message confidentiality failed.")
    else:
        print("Message confidentiality passed.")
    
    try:
        with open("client_public.pem", "rb") as f:
            CLIENT_PUB_KEY = rsa.PublicKey.load_pkcs1(f.read())
        rsa.verify(msg.encode("utf-8"), hash_digest_signature, CLIENT_PUB_KEY)
    except:
        print("Message integrity & sender authentication failed.")
    else:
        print("Message integrity & sender authentication passed.")
    
    try:
        print(msg)
    except:
        print("Unable to print out message.")


def main():
    HEADERSIZE = 10

    if len(sys.argv) > 1:
        if sys.argv[1] == "gen_key_pair":
            gen_key_pair()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 8000))
    s.listen(1)

    if len(sys.argv) > 1:
        print("Invalid command")

    while True:
        client_socket, client_address = s.accept()
        
        print(f"Connection from {client_address} has been established.")
        client_socket.send(bytes(f"Connected to server {socket.gethostname()}:{s.getsockname()[1]}.", "utf-8"))

        client_request = client_socket.recv(1024).decode("utf-8")
        if client_request == 'send_msg':
            receive_message(
                c_socket = client_socket
            )
        elif client_request == 'recv_msg':
            send_message(
                c_socket = client_socket,
                msg="This is a message from the server!"
            )
        else:
            print(f"Client typed in an invalid command: {client_request}")

        client_socket.close()


if __name__ == "__main__":
    main()
