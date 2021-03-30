from cryptography.fernet import Fernet

### This should be incorporated with the GUI ##
### If statements should be added once multiple encryption methods are added ###

key = " "

systemInfoEncrypted = 'systemInfoEncrypted.txt'
loggedKeysEncrypted = 'loggedKeysEncrypted.txt'



encryptedFiles = [systemInfoEncrypted, loggedKeysEncrypted]
count = 0


for decryptingFiles in encryptedFiles:

    with open(encryptedFiles[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open("decryption.txt", 'ab') as f:
        f.write(decrypted)

    count += 1