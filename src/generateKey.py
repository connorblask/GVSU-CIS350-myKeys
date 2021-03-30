from cryptography.fernet import Fernet

### This should be incorporated with the GUI ###
### If statements should be added once multiple encryption methods are added ###
key = Fernet.generate_key()
file = open("encryption_key.txt", 'wb')
file.write(key)
file.close()
