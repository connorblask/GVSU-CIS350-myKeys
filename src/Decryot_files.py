import base64

import gnupg
from Cryptodome.Cipher import DES3, AES
from cryptography.fernet import Fernet

BS = 16
PAD = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf-8')
UNPAD = lambda s: s[:-ord(s[len(s) - 1:])]
BLOCK_SIZE = 128
Path_to_folder = 'C:\\Users\\User\\Documents\\Winter2021\\cis350\\myKeys\\'


def decrypt_pgp(paser, encrypt_file):
    gpg = gnupg.GPG(gnupghome=Path_to_folder + 'GVSU-CIS350-myKeys\\src\\bin',
                    gpgbinary=Path_to_folder + 'GVSU-CIS350-myKeys\\src\\bin\\gpg.exe')
    # decrypt file__encrypt_file
    with open(encrypt_file, 'rb') as f:
        status = gpg.decrypt_file(
            file=f,
            passphrase=paser,
            output=encrypt_file,
        )


def des3_decrypt(key, filename, iv):
    with open(filename, 'rb') as f:
        data = f.read()
    cipher_decrypt = DES3.new(key, DES3.MODE_OFB, iv)
    with open(filename, 'wb') as f:
        f.write(cipher_decrypt.decrypt(data))


def decrypt_aes(encrypt_file, key):
    # decrypt the file with the key and aes and return the decrypt text
    with open(encrypt_file, 'rb') as files:
        data = files.read()
    data = base64.b64decode(data)
    iv = data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    with open(encrypt_file, 'wb') as f:
        f.write(UNPAD(cipher.decrypt(data[16:])))

    # decrypt from fernet


def decryptFernet(key):
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
