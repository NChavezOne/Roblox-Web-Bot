#=========================
#Imports.

import mysql.connector
import datetime
import time
import cprint

#========================= 
#Global Defines.

global scope
scope = False #Change depending on if inside or outside local network

if (scope == True):
    main_host = "98.242.199.97" #Public IP
elif (scope == False):
    main_host = "10.0.0.9" #Local IP

global mydb
mydb = mysql.connector.connect(
      host=main_host,
      user="root",
      password="alexander53",
      database="maindatabase"
    )

global now
now = datetime.datetime.now()

global iso_time
iso_time = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")

global unix_time
unix_time = int(time.time())

global clientCreated
clientCreated = True;

#==================================

def createNewClient(uuid, ipaddress, internalip):
    mycursor = mydb.cursor()

    sql = "INSERT INTO clientconnector (uuid, timecreated, lastpinged, status, ipaddress, internalip) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (uuid, iso_time, unix_time, str(0), ipaddress, internalip)
    mycursor.execute(sql, val)

    mydb.commit()
    cprint.printColor("Client added to MySQL.", "CYAN")
    
def checkIfClientExists(uuid, publicip, privateip):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM clientconnector WHERE uuid = %s AND ipaddress = %s AND internalip = %s"
    val = (uuid, publicip, privateip)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if (len(myresult) >= 1):
        if (myresult[0][0] == uuid):
            return True
    else:
        return False
    
def pingClient(uuid, os_name, commited):
    mycursor = mydb.cursor()

    global unix_time
    unix_time = int(time.time())

    sql = "UPDATE clientconnector SET lastpinged = %s WHERE uuid = %s"
    val = (unix_time, uuid) #We are pinging in unix time, seconds.
    mycursor.execute(sql, val)
    
    mydb.commit()
    
    sql = "UPDATE clientconnector SET osname = %s WHERE uuid = %s"
    val = (os_name, uuid) #We are pinging in unix time, seconds.
    mycursor.execute(sql, val)
    
    mydb.commit()
    
    sql = "UPDATE clientconnector SET commit = %s WHERE uuid = %s"
    val = (commited, uuid) #We are pinging in unix time, seconds.
    mycursor.execute(sql, val)
    
    mydb.commit()

def getLastPing(uuid):
    mycursor = mydb.cursor()
    
    sql = ("SELECT lastpinged FROM clientconnector WHERE uuid = %s")
    val = (uuid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return myresult[0][0]

def isUuidUsed(uuid):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM clientconnector WHERE uuid = %s"
    val = (uuid,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if (len(myresult) >= 1):
        return True
    else:
        return False
        
def checkIfSameIP(public,local):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM clientconnector WHERE ipaddress = %s AND internalip = %s"
    val = (public,local)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if (len(myresult) >= 1):
        return myresult[0][0]
    else:
        return False
        

#Client connector end.
#==============================

def getRandomGroup():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT groupspam FROM groupstospam ORDER BY RAND() LIMIT 1")
    myresult = mycursor.fetchall()
    group = myresult[0][0]
    return group

def getMode():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT mode FROM spambotmode ORDER BY time DESC LIMIT 1")
    myresult = mycursor.fetchall()
    mode = myresult[0][0]
    return mode

def getAccount():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT username,password FROM robloxaccounts ORDER BY RAND() LIMIT 1")
    myresult = mycursor.fetchall()
    username = myresult[0][0]
    password = myresult[0][1]
    return username, password

def insertMachineLearning(messagessent,captchasuccess):
    mycursor = mydb.cursor()

    sql = "INSERT INTO machinelearning (messagessent, captchasuccess, time) VALUES (%s, %s, %s)"
    val = (messagessent,captchasuccess, str(now))
    mycursor.execute(sql, val)

    mydb.commit()
    
    print("")
    print("MySQLConnector: The datetime is ")
    print(now)
    
    cprint.printColor("Machine learning inserted.","CYAN")
    print("")

def getRecentGroup():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT groupspam FROM spamgroup ORDER BY time DESC LIMIT 1")
    
    myresult = mycursor.fetchall()[0]
    return myresult[0]

def getRecentMessage():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT message FROM spammessage ORDER BY time DESC LIMIT 1")
    
    myresult = mycursor.fetchall()[0]
    return myresult[0]

def insertAccount(username, password):
    mycursor = mydb.cursor()

    #need to include the ` symbole for columns in the table that have a space in their name, apparently
    sql = "INSERT INTO robloxaccounts (username, password, timecreated) VALUES (%s, %s, %s)"
    val = (username, password, str(now))
    mycursor.execute(sql, val)
    
    mydb.commit()
    cprint.printColor("Account inserted","CYAN")
    
def Average(lst):
    return sum(lst) / len(lst)
 
if __name__ == "__main__":    
    
    print(getMode())
    print(getRandomGroup())
    print(getLastPing("b4da690f-235f-11ed-850e-04421a0c938c"))
