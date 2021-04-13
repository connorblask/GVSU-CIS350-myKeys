import base64

import gnupg
from Cryptodome.Cipher import DES3, AES

BS = 16
PAD = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf-8')
UNPAD = lambda s: s[:-ord(s[len(s) - 1:])]
BLOCK_SIZE = 128


class Decrypt:
    def __init__(self):
        self.gpg = gnupg.GPG(gnupghome='C:\\Program Files (x86)\\GnuPG\\bin',
                             gpgbinary='C:\\Program Files (x86)\\GnuPG\\bin\\gpg.exe')

    def decrypt_pgp(self, paser, encrypt_file, decrypt_file):
        gpg = gnupg.GPG(gnupghome='C:\\Program Files (x86)\\GnuPG\\bin',
                        gpgbinary='C:\\Program Files (x86)\\GnuPG\\bin\\gpg.exe')
        # decrypt file__encrypt_file
        with open(encrypt_file, 'rb') as f:
            status = gpg.decrypt_file(
                file=f,
                passphrase=paser,
                output=decrypt_file,
            )

    def des3_decrypt(self, key_des, iv, decrypt_file, encrypt_file):
        with open(encrypt_file, 'rb') as files:
            data = files.read()
        cipher_decrypt = DES3.new(key_des, DES3.MODE_OFB, iv)
        with open(decrypt_file, 'wb') as f:
            f.write(cipher_decrypt.decrypt(data)[:(len(cipher_decrypt.decrypt(data)) - 1)])

    def decrypt_aes(self,encrypt_file, decrypt_file, key):
        # decrypt the file with the key and aes and return the decrypt text
        with open(encrypt_file, 'rb') as files:
            data = files.read()
        data = base64.b64decode(data)
        iv = data[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        with open(decrypt_file, 'wb') as f:
            f.write(UNPAD(cipher.decrypt(data[16:])))
        return UNPAD(cipher.decrypt(data[16:]))