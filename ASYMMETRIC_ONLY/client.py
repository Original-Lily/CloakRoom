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


def send_message(s, msg):
    with open("client_private.pem", "rb") as f:
        CLIENT_PRV_KEY = rsa.PrivateKey.load_pkcs1(f.read())
    hash_digest_signature = rsa.sign(msg.encode("utf-8"), CLIENT_PRV_KEY, "SHA-256")

    with open("server_public.pem", "rb") as f:
        SERVER_PUB_KEY = rsa.PublicKey.load_pkcs1(f.read())
    encr_msg = rsa.encrypt(msg.encode("utf-8"), SERVER_PUB_KEY)
    
    s.send(hash_digest_signature)
    s.recv(1024)
    s.send(encr_msg)
    s.recv(1024)

    print("\nIntercepting the message while in transit would look like this:")
    print(encr_msg)
    print("\nIntercepting the digital signature while in transit would look like this:")
    print(hash_digest_signature)


def receive_message(s):
    signature = s.recv(10240)
    s.send(bytes(f"Received digital signature", "utf-8"))
    msg = s.recv(10240)
    s.send(bytes(f"Received message", "utf-8"))

    try:
        with open("client_private.pem", "rb") as f:
            CLIENT_PRV_KEY = rsa.PrivateKey.load_pkcs1(f.read())
        decr_msg = rsa.decrypt(msg, CLIENT_PRV_KEY).decode("utf-8")
    except:
        print("Message confidentiality failed.")
    else:
        print("Message confidentiality passed.")

    try:
        with open("server_public.pem", "rb") as f:
            SERVER_PUB_KEY = rsa.PublicKey.load_pkcs1(f.read())
        rsa.verify(decr_msg.encode("utf-8"), signature, SERVER_PUB_KEY)
    except:
        print("Message integrity & sender authentication failed.")
    else:
        print("Message integrity & sender authentication passed.")
    
    try:
        print(decr_msg)
    except:
        print("Unable to print out message.")


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "gen_key_pair":
            gen_key_pair()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 8000))

    print(s.recv(1024).decode("utf-8"))

    if len(sys.argv) > 1:
        if sys.argv[1] == "send_msg":
            s.send(sys.argv[1].encode("utf-8"))
            send_message(s=s, msg=sys.argv[2])
        elif sys.argv[1] == "recv_msg":
            s.send(sys.argv[1].encode("utf-8"))
            receive_message(s=s)
        else:
            s.send(sys.argv[1].encode("utf-8"))
            print("Invalid command")


if __name__ == "__main__":
    main()
