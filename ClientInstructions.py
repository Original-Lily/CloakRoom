# Function to read and execute commands from a file
def readCommand(InstructionList, ssh):
    with open(InstructionList, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            
            # Stop when an empty line is reached
            if not line:
                break
            
            # Execute the command using the provided SSH connection (ssh)
            stdin, stdout, stderr = ssh.exec_command(line)
            
            # Read and print the output
            variable_output = stdout.read().decode()
            print(variable_output)
