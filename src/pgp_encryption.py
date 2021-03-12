__author__ = 'Neta'
#this class dael with des decrypt and encrypt
import files_tr


class pgp_encryption():
    def __init__(self, key, algorithm, file_name, user):
        self.key = key
        self.algorithm = algorithm
        self.data = files_tr.FilesWork.read_file(file_name)
        files_tr.FilesWork.delete_file(file_name)
        self.user = user

    def decrypt(self):
        if self.key == "":
            self.key = Keysdatabase.Usersdefault.get_keydefult(self.user)
        return self.key
    def encrypt(self):
        ##encrypt using pgp
        if self.key_type = public_key:
            return ""