from cryptography.fernet import Fernet
import rsa
import socket
import sys

###########################################################################################
# Generate a key pair for the server fucntion:
#   - Generate RSA key pairs with a length of 2048 bits.
#   - Store the public key and private key in .pem file formats.
#   - Clear keys from variables.
#   - Terminate the program to prevent socket execution.
###########################################################################################

def generate_key_pair():
    SERVER_PUB_KEY, SERVER_PRV_KEY = rsa.newkeys(2048)
    
    with open("server_public.pem", "wb") as f:
        f.write(SERVER_PUB_KEY.save_pkcs1("PEM"))
    with open("server_private.pem", "wb") as f:
        f.write(SERVER_PRV_KEY.save_pkcs1("PEM"))

    SERVER_PUB_KEY = None
    SERVER_PRV_KEY = None
    sys.exit()

###########################################################################################
# Transmit Message function:
#   - Retrieve the private key of the server.
#   - Hash the message using the SHA256 algorithm and sign the hash digest with the client's private key.
#   - Retrieve the public key of the server.
#   - Create a variable containing the signature and the message.
###########################################################################################
    
def send_msg(c_socket, msg):
    symmetric_key = Fernet.generate_key()

    with open("server_private.pem", "rb") as f:
        SERVER_PRV_KEY = rsa.PrivateKey.load_pkcs1(f.read())
    hash_digest_signature = rsa.sign(msg.encode("utf-8"), SERVER_PRV_KEY, "SHA-256")
    with open("client_public.pem", "rb") as f:
        CLIENT_PUB_KEY = rsa.PublicKey.load_pkcs1(f.read())

    data_block = [list(hash_digest_signature), msg]

    #ENCRYPT USING SYMMETRIC KEY
    encr_data_block = Fernet(symmetric_key).encrypt(bytes(str(data_block).encode("utf-8")))
    #ENCRYPT USING CLIENT PUBLIC KEY
    encr_symmetric_key = rsa.encrypt(symmetric_key, CLIENT_PUB_KEY)

    c_socket.send(encr_symmetric_key)
    c_socket.recv(1024)   
    c_socket.send(encr_data_block)
    c_socket.recv(1024)   

    #PROOF OF ENCRYPTION
    print("\nIntercepting the data block while in transit would look like this:")
    print(encr_data_block)
    print("\nIntercepting the symmetric key while in transit would look like this:")
    print(hash_digest_signature)

###########################################################################################
# Accept Message function:
#   - Accept the encrypted key & variable holding signature & message.
#   - Retrieve the private key of the server.
#   - Decrypt the symmetric key using the server's private key.
#   - Use the symmetric key to decrypt the data block.
#   - Separate the variables in the data block.
#   - Retrieve the public key of the client.
#   - Verify the hash digest signature using the client's public key.
#   - Display the decrypted message.
###########################################################################################
  
def recv_msg(c_socket):
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

###########################################################################################
# Main function:
#   - Create a socket object with AF_INET (IPv4) family type and SOCK_STREAM (TCP) socket type.
#   - Associate the socket with the hostname of this computer, on port 8000.
#   - Set a backlog queue of 1. For illustration, we will handle one client at a time.
#   - While the server is active...
#       - Accept client socket connections, store the client socket object, and its source address.
#       - Display the client's address.
#       - Inform the client about the successful connection to the server.
#       - Receive the client's request.
#       - Perform functions such as sending and receiving messages.
#       - If the client's request is invalid, print an error message.
#       - Close the socket after the last request between the client and server.
###########################################################################################
   
def main():
    # Checking the command line for arguments.
    if len(sys.argv) > 1:
        # If the first arg (the command) is requesting to generate keys...
        if sys.argv[1] == "generate_key_pair":
            generate_key_pair()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 8000))
    s.listen(1)

    # Checking the command line for arguments.
    if len(sys.argv) > 1:
        print("Invalid command")

    while True:
        client_socket, client_address = s.accept()
        print(f"Connection from {client_address} has been established.")
        client_socket.send(bytes(f"Connected to server {socket.gethostname()}:{s.getsockname()[1]}.", "utf-8"))

        client_request = client_socket.recv(1024).decode("utf-8")

        if client_request == 'send_msg':             
            recv_msg(
                c_socket = client_socket
            )
        elif client_request == 'recv_msg':
            send_msg(
                c_socket = client_socket,
                msg="This is a message from the server!"
            )
        else:
            print(f"Client typed in an invalid command: {client_request}")

        client_socket.close()

###########################################################################################

if __name__ == "__main__":
    main()