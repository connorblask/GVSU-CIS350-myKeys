import gnupg


# This should be incorporated with the GUI ###
# If statements should be added once multiple encryption methods are added ###

class GenerateKeyPgp:

    def __init__(self, email, passphrase):
        # initial the root for the gpg files
        self.gpg = gnupg.GPG(gnupghome='C:\\Program Files (x86)\\GnuPG\\bin',
                             gpgbinary='C:\\Program Files (x86)\\GnuPG\\bin\\gpg.exe')
        self.filekeys_path = '/check_folder/mykeyfile.asc'
        self.email_name = email
        self.paser = passphrase

    @staticmethod
    def create_key(self):
        # generate key
        input_data = self.gpg.gen_key_input(key_type="RSA",
                                            key_length=2048,
                                            name_email=self.email_name,
                                            passphrase=self.paser)
        self.key = self.gpg.gen_key(input_data)
        print(self.key)

    def import_asci(self):
        # creating ascii version of the public and private keys
        ascii_armored_public_keys = self.gpg.export_keys(self.key.fingerprint)
        ascii_armored_private_keys = self.gpg.export_keys(
            keyids=self.key.fingerprint,
            secret=True,
            passphrase=self.paser,
        )
        # export mykeyfile.asc'
        # par filekeys_path contains path+name+asc
        with open(self.filekeys_path, 'w') as f:
            f.write(ascii_armored_public_keys)
            f.write(ascii_armored_private_keys)

    @staticmethod
    def get_key_ascifile(self):
        # import from ascii file to find the key
        with open(self.filekeys_path) as f:
            key_data = f.read()
        import_result = self.gpg.import_keys(key_data)
        for k in import_result.results:
            print(k)

    def encrypt_pgp(self, original_file, encrypt_file):
        # encrypt file name original_file
        # output in the dir and the encrypt file that we entered
        with open(original_file, 'rb') as f:
            status = self.gpg.encrypt_file(
                f, recipients=[self.email_name],
                output=encrypt_file + '.gpg')
        print(status.ok)
        print(status.status)
        print(status.stderr)
        print('~' * 50)

    def decrypt_pgp(self, encrypt_file, decrypt_file):
        # decrypt file__encrypt_file
        with open(encrypt_file, 'rb') as f:
            status = self.gpg.decrypt_file(
                file=f,
                passphrase=self.paser,
                output=decrypt_file,
            )
