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
finally:
    clientsocket.close()

print (data.decode())