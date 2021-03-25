#File Client
import socket
import sys

#setting up proper vars
print("Welcome to myKeys!\n")
server_ip = input("Server IP address: ")
server_port = input("Port number: ")
buffer_size = 1024

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    print("Connecting to " + server_ip + " on port " + server_port + "\n")
    clientsocket.connect((server_ip, int(server_port)))
    data = clientsocket.recv(buffer_size)
    print (data.decode())
    while(True):
        user_command = input("\n Enter a command: \n")
        user_command.replace(" ", "")
        if user_command[0:4] == "pull":
            _pull_file(user_command)
        elif user_command[0:4] == "quit":
            sent_data = "quit"
            clientsocket.send(sent_data.encode())
            break
        else:
            print("Command not understood.\n")

finally:
    clientsocket.close()

def _pull_file(user_command):
    filename = user_command[4:]
    sent_data = ("pull" + filename)
    clientsocket.send(sent_data.encode())
    status = clientsocket.recv(buffer_size)
    if status.decode() == "failure":
        print("Failed to retreive file.\n")
    elif status.decode() == "success":
        print("Downloading file...\n")
        f = open (filename, 'wb')
        l = clientsocket.recv(buffer_size)
        while(l):
            f.write(l)
            l = clientsocket.recv(buffer_size)


