# myKeys

## Introduction

myKeys will be a keylogger designed for offensive security testing. The program will be split into two parts, a server and a client. The client side will be the keylogger that records all keystrokes, and saves them in a file. The file will be able to be encrypted or encoded before being sent to the user. The user will be able to choose whatever method of encryption or encoding is best for their needs. The client will communicate with the server regularly, sending it the encrypted or encoded logged information. The server’s role will be to receive this data, decrypt it, and present it for the user with a readable GUI.

## Anticipated Technologies

* The program will be written in Python
* Strong encryption method for stored data
* GUI for showing the data to the user on the server end
* CLI for setting up target end of program
* Network communication between target and server using a secure protocol (TBD)
* Google cloud for hosting server

## Method/Approach

* Scrum/Agile with Trello board
* Post tasks to trello board as necessary
* Tasks can be tagged for your own group or for other groups
    

## Estimated Timeline

* Week 1: Determine small groups and specific technologies (protocols, encryption methods)
* Week 2-3: Begin programming in small groups
* Week 4: First round of thorough testing
* Week 5-6: Finish small group responsibilities
* Week 7-8: Testing everything together

## Anticipated Problems

* Transferring text files to the cloud
* Getting the target-side program installed


## Team Members and Roles

* [Neta Shiff](https://github.com/netashiff/CIS-HM2-Shiff.git)
* [Brenden Richardson](https://github.com/BrendenRichardson/CIS350-HW2-Richardson.git)
* [Connor Blaszkiewicz](https://github.com/connorblask/CIS350-HW2-Blaszkiewicz/)
* [Brendan O'Brien](https://github.com/brendan7255/CIS350-HW2-Obrien)
* [Ben Jenkins](https://github.com/benjaminjenkins/CIS350-HW2-jenkins)

## Prerequisites
### GUI and Payload
* Install Gnupg -  on your computer via the website https://gnupg.org/download/

* enter to your command line and Pip for gnupg, Cryptodome, pynupt, cryptography, requests  

* make sure that the path to the project and for gnupg is the same as written inside the code
### Cloud
* The cloud machine must have python installed    

## Run Instructions
#### GUI
* Run the GUI.py file
* Use the configuration tab in the GUI to create a config file
* Connect to server through GUI download tab (IP: 35.231.244.179)
* Enter files you want to download
* Decrypt file through decrypt tab using generated key (bottom of config tab)
### Cloud
* Run the python files (tcp_server.py and udp_server.py) from the command line
### Payload
* Download the keylogger file and the generated config file to the same directory
* Run the keylogger.py payload


