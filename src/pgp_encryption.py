
class pgp_enctyption:

    def __init__(self, key, algorithm, file_name, user):
        self.key = key
        self.algorithm = algorithm
        self.data = files_tr.FilesWork.read_file(file_name)
        files_tr.FilesWork.delete_file(file_name)
        self.user = user

    def ifkey(self):
        if self.key == "":
            self.key = Keysdatabase.Usersdefault.get_keydefault(self.user)
        return self.key