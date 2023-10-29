import paramiko
import ClientInstructions

# Define your VM's SSH details
hostname = 'ec2-16-170-250-209.eu-north-1.compute.amazonaws.com'
username = 'Client'
private_key_path = 'UbuntuChatKey.pem'  # Replace with the path to your key file

# Initialize an SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Load the private key
    private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

    # Connect to the VM using key-based authentication
    ssh.connect(hostname, username=username, pkey=private_key)

    #text file containing list of instructions to be exeuted
    filename = 'InstructionsList.txt'

    ClientInstructions.readCommand(filename, ssh)

except paramiko.AuthenticationException:
    print("Authentication failed")
except paramiko.SSHException as e:
    print("SSH connection failed:", str(e))
except Exception as e:
    print("An error occurred:", str(e))
finally:
    # Close the SSH connection
    ssh.close()
