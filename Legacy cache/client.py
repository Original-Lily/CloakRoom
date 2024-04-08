from cryptography.fernet import Fernet
import rsa, socket, sys

#########################################################################################
# Generate a key pair for the client fucntion:
#   - Generate RSA key pairs with a length of 2048 bits.
#   - Store the public key and private key in .pem file formats.
#   - Clear keys from variables.
#   - Terminate the program to prevent socket execution.
#########################################################################################

def generate_key_pair():
    CLIENT_PUB_KEY, CLIENT_PRV_KEY = rsa.newkeys(2048)

    with open("client_public.pem", "wb") as f:
        f.write(CLIENT_PUB_KEY.save_pkcs1("PEM"))
    with open("client_private.pem", "wb") as f:
        f.write(CLIENT_PRV_KEY.save_pkcs1("PEM"))

    CLIENT_PUB_KEY = None
    CLIENT_PRV_KEY = None
    sys.exit()

#########################################################################################
# Send a message to the server function:
#   - Encrypt the message using the generated key.
#   - Encrypt the symmetric key using the server's public key.
#   - Send the encrypted symmetric key and encrypted message to the server.
#   - Print out the encrypted message.
#########################################################################################

def send_msg(socket, msg):
    symmetric_key = Fernet.generate_key()

    with open("client_private.pem", "rb") as f:
        CLIENT_PRV_KEY = rsa.PrivateKey.load_pkcs1(f.read())
    hash_digest_signature = rsa.sign(msg.encode("utf-8"), CLIENT_PRV_KEY, "SHA-256")
    with open("server_public.pem", "rb") as f:
        SERVER_PUB_KEY = rsa.PublicKey.load_pkcs1(f.read())
        
    data_block = [list(hash_digest_signature), msg]
    
    #ENCRYPT USING SYMMETRIC KEY
    encr_data_block = Fernet(symmetric_key).encrypt(bytes(str(data_block).encode("utf-8")))
    #ENCRYPT USING SERVER PUBLIC KEY
    encr_symmetric_key = rsa.encrypt(symmetric_key, SERVER_PUB_KEY)

    socket.send(encr_symmetric_key)
    socket.recv(1024)  
    socket.send(encr_data_block)
    socket.recv(1024)   

    #PROOF OF ENCRYPTION
    print("\nIntercepting the data block while in transit would look like this:")
    print(encr_data_block)
    print("\nIntercepting the symmetric key while in transit would look like this:")
    print(hash_digest_signature)

#########################################################################################
# Receive a message from the server function:
#   - Request the encrypted symmetric key and data block from the server
#   - Send acknowledgment confirmations to the server.
#   - Decrypt the symmetric key & data using the client's private key.
#   - Verify the hash digest signature using the server's public key.
#   - Print out the decrypted message.
#########################################################################################

def recv_msg(socket):
    encr_symmetric_key = socket.recv(10240)
    socket.send(bytes(f"Received symmetric key", "utf-8"))
    encr_data_block = socket.recv(10240)
    socket.send(bytes(f"Received data block", "utf-8"))

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

#########################################################################################
# Main function:
#   - If the client desires to generate keys, execute the corresponding function.
#   - Create a socket object with AF_INET (IPv4) family type and SOCK_STREAM (TCP) socket type.
#   - Establish a connection to the server (this computer) on port 8000.
#   - Notify the client about the successful connection.
#   - Check the command line for arguments:
#       - If the first argument (the command) requests sending a message to the server...
#           - Execute the corresponding function with the message to send.
#       - If the first argument (the command) requests receiving a message from the server...
#           - Execute the corresponding function.
#       - If the first argument (the command) is invalid, inform the client.
#########################################################################################

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "generate_key_pair":
            generate_key_pair()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 8000))

    print(s.recv(2048).decode("utf-8"))

    if len(sys.argv) > 1:
        if sys.argv[1] == "send_msg":
            s.send(sys.argv[1].encode("utf-8"))
            send_msg(socket=s, msg=sys.argv[2])
        elif sys.argv[1] == "recv_msg":
            s.send(sys.argv[1].encode("utf-8"))
            recv_msg(socket=s)
        else:
            s.send(sys.argv[1].encode("utf-8"))
            print("Invalid command")

###########################################################################################
            
# Run the code
if __name__ == "__main__":
    main()
