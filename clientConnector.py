#====================
#Imports

import os
import uuid
import urllib.request
import socket

import MySQLConnector

#====================
#Global defines
global uuid_global

global external_ip
external_ip = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8')

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
global internal_ip 
internal_ip = get_ip_address()

def genUuid():
    return str(uuid.uuid1())
    
def connectToSQLClientService():
    global uuid_global
    myFile = r"Client Identifier/uuid.txt"
    if (os.path.isfile(myFile)):
        file = open(myFile,"r")
        temp = file.read()
        file.close()
        if (len(temp) < 10):
            file.close()
            file = open(myFile,"w")
            uuid_global = genUuid()
            print(uuid_global)
            file.write(uuid_global)
            file.close()
        else:
            uuid_global = temp
        print("Client exists!")
        if (MySQLConnector.checkIfClientExists(uuid_global, external_ip, internal_ip) == True):
            print("Pinging client!")
            MySQLConnector.pingClient(uuid_global)
        else:
            MySQLConnector.createNewClient(uuid_global, external_ip, internal_ip)
            print("We've created a new client.")
    else:
        file = open(myFile,"w")
        uuid_global = genUuid()
        file.write(uuid_global)
        file.close()
        MySQLConnector.createNewClient(uuid_global, external_ip)
        print("We've created a new client.")
    
def pingClient():
    MySQLConnector.pingClient(uuid_global)
    print("Client service pinged.")
    time.sleep(5)
    pingClient()

if __name__ == "__main__":
    
    import threading
    import time
    
    print("clientConnector script running as main!")
    connectToSQLClientService()
    
    pingservice = threading.Thread(target=pingClient,args=(),daemon=True)
    pingservice.start()
    
    while (1):
        print("Doing other stuff kek")
        time.sleep(0.1)
        
