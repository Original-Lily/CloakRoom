from cryptography.fernet import Fernet
import rsa
import socket
import sys


def gen_key_pair():
    CLIENT_PUB_KEY, CLIENT_PRV_KEY = rsa.newkeys(2048)

    with open("client_public.pem", "wb") as f:
        f.write(CLIENT_PUB_KEY.save_pkcs1("PEM"))

    with open("client_private.pem", "wb") as f:
        f.write(CLIENT_PRV_KEY.save_pkcs1("PEM"))

    CLIENT_PUB_KEY = None
    CLIENT_PRV_KEY = None

    sys.exit()


def send_message(sock, msg):
    symmetric_key = Fernet.generate_key()

    with open("client_private.pem", "rb") as f:
        CLIENT_PRV_KEY = rsa.PrivateKey.load_pkcs1(f.read())
    hash_digest_signature = rsa.sign(msg.encode("utf-8"), CLIENT_PRV_KEY, "SHA-256")

    with open("server_public.pem", "rb") as f:
        SERVER_PUB_KEY = rsa.PublicKey.load_pkcs1(f.read())
    data_block = [list(hash_digest_signature), msg]

    encr_data_block = Fernet(symmetric_key).encrypt(bytes(str(data_block).encode("utf-8")))
    encr_symmetric_key = rsa.encrypt(symmetric_key, SERVER_PUB_KEY)

    sock.send(encr_symmetric_key)
    sock.recv(1024)
    sock.send(encr_data_block)
    sock.recv(1024)

    print("\nIntercepting the data block while in transit would look like this:")
    print(encr_data_block)
    print("\nIntercepting the symmetric key while in transit would look like this:")
    print(hash_digest_signature)


def receive_message(sock):
    encr_symmetric_key = sock.recv(10240)
    sock.send(bytes(f"Received symmetric key", "utf-8"))
    encr_data_block = sock.recv(10240)
    sock.send(bytes(f"Received data block", "utf-8"))

    try:
        with open("client_private.pem", "rb") as f:
            CLIENT_PRV_KEY = rsa.PrivateKey.load_pkcs1(f.read())
        decr_symmetric_key = rsa.decrypt(encr_symmetric_key, CLIENT_PRV_KEY)

        decr_data_block = Fernet(decr_symmetric_key).decrypt(encr_data_block).decode("utf-8")
        hash_digest_signature = bytes([int(i) for i in decr_data_block[2:decr_data_block.find("], '")].split(", ")])
        msg = decr_data_block[decr_data_block.find("], '") + 4:-2]
    except:
        print("Message confidentiality failed.")
    else:
        print("Message confidentiality passed.")
    
    try:
        with open("server_public.pem", "rb") as f:
            SERVER_PUB_KEY = rsa.PublicKey.load_pkcs1(f.read())
        rsa.verify(msg.encode("utf-8"), hash_digest_signature, SERVER_PUB_KEY)
    except:
        print("Message integrity & sender authentication failed.")
    else:
        print("Message integrity & sender authentication passed.")
    
    try:
        print(msg)
    except:
        print("Unable to print out message.")


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "gen_key_pair":
            gen_key_pair()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 8000))

    print(s.recv(2048).decode("utf-8"))

    if len(sys.argv) > 1:
        if sys.argv[1] == "send_msg":
            s.send(sys.argv[1].encode("utf-8"))
            send_message(sock=s, msg=sys.argv[2])
        elif sys.argv[1] == "recv_msg":
            s.send(sys.argv[1].encode("utf-8"))
            receive_message(sock=s)
        else:
            s.send(sys.argv[1].encode("utf-8"))
            print("Invalid command")


if __name__ == "__main__":
    main()
