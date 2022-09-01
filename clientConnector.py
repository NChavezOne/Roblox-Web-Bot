#====================
#Imports

import os
import uuid
import urllib.request
import socket

import MySQLConnector

import time

#====================
#Global defines
global pingservice

global device_name
device_name = os.environ['COMPUTERNAME']

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
            #print(uuid_global)
            file.write(uuid_global)
            file.close()
        else:
            uuid_global = temp
        #print("Client exists!")
        val = MySQLConnector.checkIfSameIP(external_ip, internal_ip)
        if (MySQLConnector.checkIfClientExists(uuid_global, external_ip, internal_ip) == True):
            print("Pinging client!")
            MySQLConnector.pingClient(uuid_global, device_name)
        elif (val != False):
            print("Pinging client!")
            file = open(myFile,"w")
            uuid_global = val
            file.write(uuid_global)
            file.close()
            MySQLConnector.pingClient(uuid_global, device_name)
        else:
            if (MySQLConnector.isUuidUsed(uuid_global) == False):
                
                MySQLConnector.createNewClient(uuid_global, external_ip, internal_ip)
            else: 
                file = open(myFile,"w")
                uuid_global = genUuid()
                #print(uuid_global)
                file.write(uuid_global)
                file.close()
                MySQLConnector.createNewClient(uuid_global, external_ip, internal_ip)
            #print("We've created a new client.")
    else:
        file = open(myFile,"w")
        uuid_global = genUuid()
        file.write(uuid_global)
        file.close()
        MySQLConnector.createNewClient(uuid_global, external_ip)
        print("We've created a new client.")
    global pingservice
    
def pingClient(uuid):
    while(1):
        MySQLConnector.pingClient(uuid, device_name)
        print("Client service pinged.")
        time.sleep(5)
        
def beginPingService():
    global pingservice
    pingservice.start()
    print("Starting pingservice.")
    
def endPingService():
    global pingservice
    pingservice.terminate()
    print("Killing pingservice.")

def returnUuid():
    global uuid_global
    return uuid_global

if __name__ == "__main__":

    print("Client connector script running as main!")
    
    connectToSQLClientService()
    beginPingService()
