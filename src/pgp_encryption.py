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


#the class can read and delete files
import os
PATH = 'C:'#FIND THE RIGHT PATH


class FilesWork:
    def __init__(self, file_name):
        self.name_file = file_name

    @staticmethod
    def delete_file(name_file):
    ## if file exists, delete it ##
        if os.path.isfile(PATH + name_file):
                os.remove(name_file)
        else:
         ## Show an error
                print("Error: %s file not found" % name_file)

    @staticmethod
    def read_file(name_file):
        with open(PATH + name_file, 'rb') as files:
            data = files.read()
        FilesWork.delete_file(name_file)
        return data