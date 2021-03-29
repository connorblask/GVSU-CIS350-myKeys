import gnupg


class Decrypt:
    def __init__(self):
        self.gpg = gnupg.GPG(gnupghome='C:\\Program Files (x86)\\GnuPG\\bin',
                             gpgbinary='C:\\Program Files (x86)\\GnuPG\\bin\\gpg.exe')

    def decrypt_pgp(self, paser, encrypt_file, decrypt_file):
        # decrypt file__encrypt_file
        with open(encrypt_file, 'rb') as f:
            status = self.gpg.decrypt_file(
                file=f,
                passphrase=paser,
                output=decrypt_file,
            )
