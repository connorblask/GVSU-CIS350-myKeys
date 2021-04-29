#File Client
import socket
import sys

#setting up proper vars
print("Welcome to myKeys!\n")
server_ip = input("Server IP address: ")
server_port = input("Port number: ")
buffer_size = 1024

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def pull_file(user_command):
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
            sent_data = "received".encode()
            clientsocket.send(sent_data)
            if (l.decode()[0:3] == "eof"):
                break
            elif (l.decode()[0:3] == "con"):
                l = l[3:]
                f.write(l)
                l = clientsocket.recv(buffer_size)
        f.close()
        print("Download complete!\n")
        return
    else:
        print('Received unexpected message.')
        return

try:
    print("Connecting to " + server_ip + " on port " + server_port + "\n")
    clientsocket.connect((server_ip, int(server_port)))
    data = clientsocket.recv(buffer_size)
    print (data.decode())
    while(True):
        user_command = input("\nEnter a command: \n")
        user_command = user_command.replace(" ", "")
        if user_command[0:4] == "pull":
            pull_file(user_command)
        elif user_command[0:4] == "quit":
            sent_data = "quit"
            clientsocket.send(sent_data.encode())
            break
        else:
            print("Command not understood.\n")

finally:
    clientsocket.close()




