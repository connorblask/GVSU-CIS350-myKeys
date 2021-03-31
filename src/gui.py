#Team myKeys
#myKeysGUI.py
#Brenden Richardson

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

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

        # Configuration Tab 
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

        # check buttons
        def startFunction():
            if (check1.get() == 0) & (check2.get() == 0):
                 messagebox.showwarning('Invalid Entry', 'Must choose at least 1 selection for file retrieval')

        # checkbutton for system info
        sysButton = ttk.Checkbutton(configTab, text='System Info', variable=check1)
        sysButton.pack(expand=1, fill="both")
        
        # checkbutton for keylogger
        keyLButton = ttk.Checkbutton(configTab, text='Keylogger', variable=check2)
        keyLButton.pack(expand=1, fill="both")
    
        #file path function
        #def filePath():
        #    file = filedialog.askopenfilename()

        # filedialog chooser
        # pathButton = tk.Button(configTab, text='File Path', command=filePath)
        # pathButton.pack(expand=1, fill="both")

        # button to start program
        startButton = tk.Button(configTab, text='Start', command=startFunction)
        startButton.pack(expand=1, fill="both")

        # label for generated key
        keyGenLbl = ttk.Label(configTab, text='Generated Key:')
        keyGenLbl.pack(expand=1, fill="both")

        generatedKey = ''
        
        # decryption key
        decryptKeyLbl = ttk.Label(configTab,background="white", textvariable=generatedKey)
        decryptKeyLbl.pack(expand=1, fill="both")

        # Decryption Tab
        # decryption type label
        decryptLbl = ttk.Label(decryptionTab, text='Decryption Type')
        decryptLbl.pack(expand=1, fill="both")

        # decryption dropdown menu
        self.dType = tk.StringVar()
        dTypeDrop = ttk.Combobox(decryptionTab, textvariable = self.dType, state='readonly')
        dTypeDrop['values'] = ("pgp", "fernet", "DES3", "AES")
        dTypeDrop.current(0)
        dTypeDrop.pack(expand=1, fill="both")

        # decrytion key label
        decryptKeylbl = ttk.Label(decryptionTab, text='Enter Decryption Key')
        decryptKeylbl.pack(expand=1, fill="both")

        # decryption key entry box
        keyVar = tk.IntVar()
        keyEntry = ttk.Entry(decryptionTab, textvariable=keyVar)
        keyEntry.pack(expand=1, fill="both")

        # decryption start button
        decryptStartButton = tk.Button(decryptionTab, text='Start')
        decryptStartButton.pack(expand=1, fill="both")

        # Download tab
        # IP label
        ipLbl = ttk.Label(downloadTab, text='Enter IP Address')
        ipLbl.pack(expand=1, fill="both")

        # IP entry field
        ipVar = tk.StringVar()
        ipEntry = tk.Entry(downloadTab, textvariable=ipVar)
        ipEntry.pack(expand=1, fill="both")

        # connect button
        connectButton = tk.Button(downloadTab, text='Connect')
        connectButton.pack(expand=1, fill="both")

        # directory info label
        dirInfoLbl = ttk.Label(downloadTab, text='Directory Information')
        dirInfoLbl.pack(expand=1, fill="both")

        # display for directory information
        dirInfoVar = tk.StringVar()
        dirInfo = tk.Label(downloadTab, background="white", textvariable= dirInfoVar)
        dirInfo.pack(expand=1, fill="both")

        # file name label
        fileNameLbl = ttk.Label(downloadTab, text='Name of File')
        fileNameLbl.pack(expand=1, fill="both")

        # file name entry
        fileName = tk.StringVar()
        fileNameEntry = tk.Entry(downloadTab, textvariable=fileName)
        fileNameEntry.pack(expand=1, fill="both")

        #window constraints
        parent.minsize(250,150)
        #parent.maxsize(300,200)
        
if __name__ == "__main__":
    root = tk.Tk()
    MyKeysGui(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
