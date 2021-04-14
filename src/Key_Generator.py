import os
import gnupg
from Cryptodome.Cipher import DES3
from Cryptodome.Random import get_random_bytes


class Generation:
    def __init__(self):
        pass

    def pgp_generation(email, pashprase):
        gpg = gnupg.GPG(gnupghome='C:\\Program Files (x86)\\GnuPG\\bin',
                        gpgbinary='C:\\Program Files (x86)\\GnuPG\\bin\\gpg.exe')

        input_data = gpg.gen_key_input(key_type="RSA",
                                       key_length=2048,
                                       name_email=email,
                                       passphrase=pashprase)
        key = gpg.gen_key(input_data)
        print(key)
        return key

    def DES3(self):
        key = DES3.adjust_key_parity(get_random_bytes(24))
        return key

    def generate_AES(self):
        key = os.urandom(16)
        print(key)
        return key
