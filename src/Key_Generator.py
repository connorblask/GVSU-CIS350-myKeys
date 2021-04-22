import os
import gnupg
from Cryptodome.Cipher import DES3
from Cryptodome.Random import get_random_bytes
#pip uninstall gnupg
#pip install python-gnupg
Path_to_folder ='C:\\Users\\User\\Documents\\Winter2021\\cis350\\myKeys\\'

def pgp_generation(email, passphrase):
    gpg = gnupg.GPG(gnupghome=Path_to_folder+'GVSU-CIS350-myKeys\\src\\bin',
                    gpgbinary=Path_to_folder+'GVSU-CIS350-myKeys\\src\\bin\\gpg.exe')
    input_data = gpg.gen_key_input(key_type="RSA",
                                   key_length=2048,
                                   name_email=email,
                                   passphrase=passphrase)
    key = gpg.gen_key(input_data)
    print(key)
    return key


def DES3_generation():
    key = DES3.adjust_key_parity(get_random_bytes(24))
    return key


def generate_AES():
    key = os.urandom(16)
    print(key)
    return key


print(pgp_generation("neta@gmail.com", "my pahprash"))
