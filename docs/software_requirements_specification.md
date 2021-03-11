# Overview
This is the software requirements specification (SRS) document. All of the program’s requirements are defined here. These requirements help visualize what the outcome of the final project will look like and the functionalities it will have included.
 
# Functional Requirements
 
1. Encryption

    1. The program shall be able to encrypt in PGP encryption {F1.1}
    1. The user shall have the option to encrypt a text file using the encryption methods available to them {F1.2}
    1. Software shall encrypt the text file before it is sent to the cloud software. {F1.3}
    
1. Cloud
    1. The target shall use a connectionless protocol (UDP-based) to send a new keylog file to the server every hour {F2.1}
    1. The server shall not send any packets to the target device {F2.2}
    1. The user shall utilize a TCP-based protocol to download files from the server, allowing for file viewing, selection, authentication, and encrypted communication {F2.3}
        1. The server program shall run a TCP-based server socket hosting the directory where it stores the keylog files {F2.3.1}
        1. The server program shall enforce a user account creation upon installation on the server device {F2.3.2}
        
1. GUI
    1. Users shall be able to pull the encrypted text file from a remote network through the GUI. {F3.1} 
    
1. Keylogger
     1. Software shall collect keystrokes and place them into a hidden text file. {F4.1}
     1. Every key pressed by the user shall be logged into a text file. {F4.2}

# Non-Functional Requirements
 
1. Encryption
    1. Unencrypted text files received shall not be stored or saved on the cloud software. {NF1.1}
    2. The user shall be able to choose the type of encryption. {NF1.2}
1. Cloud
    1. The files sent to the server from the target shall be transmitted accurately and without errors {NF2.1}
    1. Communication between the server and all other devices shall be authenticated so as to prevent the unwanted upload or download of files {NF2.2}
    1. Software shall be capable of handling multiple requests without affecting performance {NF2.3}
    1. The Program shall use Google Cloud as the remote network storing the files {NF2.4}
1. GUI
    1. A GUI shall be used for an easy user experience. {NF 3.1}
1. Keylogger
    1. The target-side program shall be installable through keyboard input alone so that it may be installed via a rubber ducky or similar tool {NF4.1}
    1. The software shall be portable, as long as the target machine has Python installed. {NF4.2}

