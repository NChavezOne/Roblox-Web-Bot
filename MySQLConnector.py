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
global sql_username
sql_username = "root"
global sql_password
sql_password = "poopoocaca51"

global now
now = datetime.datetime.now()

global iso_time
iso_time = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")

global unix_time
unix_time = int(time.time())

global clientCreated
clientCreated = True;

#==================================
def createConnection():
    global mydb
    try:
        mydb = mysql.connector.connect(
              host=main_host,
              user=sql_username,
              password=sql_password,
              database="maindatabase"
            )
        return True
    except:
        time.sleep(1)
        cprint.printColor("Could not find maindatabase. Waiting here, the server script should create a new one from backup.","RED")
        mydb = mysql.connector.connect(
              host=main_host,
              user=sql_username,
              password=sql_password,
            )
        mycursor = mydb.cursor()

        sql = "SHOW DATABASES"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        databases = list()
        for x in myresult:
            databases.append(x[0])
        database_found = False
        for x in databases:
            if (x == "maindatabase"):
                database_found = True
            else:
                pass
           
        if (database_found == False): 
            cprint.printColor("No database found. Waiting 60 seconds for a new one to appear.","RED")
        else:
            cprint.printColor("Could not connect to maindatabase, however it does exist","RED")
        
        return False
        
        
#==================================
def createNewClient(uuid, ipaddress, internalip):
    if createConnection():
        mycursor = mydb.cursor()

        sql = "INSERT INTO clientconnector (uuid, timecreated, lastpinged, status, ipaddress, internalip) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (uuid, iso_time, unix_time, str(0), ipaddress, internalip)
        mycursor.execute(sql, val)

        mydb.commit()
        cprint.printColor("Client added to MySQL.", "CYAN")
    
def checkIfClientExists(uuid, publicip, privateip):
    if createConnection():
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
    
def pingClient(uuid, os_name, **kwargs):
    if createConnection():
        mycursor = mydb.cursor()

        global unix_time
        unix_time = int(time.time())

        try:
            sql = "SELECT * FROM clientconnector WHERE uuid = %s"
            val = (uuid,) #Check if the client exists.
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            if (len(myresult) < 1):
                print("Client does not exist. Connecting.")
                return False
        except:
            print("Client returns error. Connecting.")
            return False

        sql = "UPDATE clientconnector SET lastpinged = %s WHERE uuid = %s"
        val = (unix_time, uuid) #We are pinging in unix time, seconds.
        mycursor.execute(sql, val)
        
        mydb.commit()
        
        sql = "UPDATE clientconnector SET osname = %s WHERE uuid = %s"
        val = (os_name, uuid) #We are pinging in unix time, seconds.
        mycursor.execute(sql, val)
        
        mydb.commit()
        
        git_commit = kwargs.get('git_commit', None)
        
        sql = "UPDATE clientconnector SET commit = %s WHERE uuid = %s"
        val = (git_commit, uuid) #We are pinging in unix time, seconds.
        mycursor.execute(sql, val)
        
        mydb.commit()

def getLastPing(uuid):
    if createConnection():
        mycursor = mydb.cursor()
        
        sql = ("SELECT lastpinged FROM clientconnector WHERE uuid = %s")
        val = (uuid,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        return myresult[0][0]

def isUuidUsed(uuid):
    if createConnection():
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
    if createConnection():
        mycursor = mydb.cursor()
        sql = "SELECT * FROM clientconnector WHERE ipaddress = %s AND internalip = %s"
        val = (public,local)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if (len(myresult) >= 1):
            return myresult[0][0]
        else:
            return False
        
def checkIfSameMic(uuid):
    if createConnection():
        mycursor = mydb.cursor()
        sql = "SELECT correctmic FROM clientconnector WHERE uuid = %s"
        val = (uuid,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if (len(myresult) >= 1):
            return myresult[0][0]
        else:
            return False
        
def setMic(uuid, mic):
    if createConnection():
        mycursor = mydb.cursor()

        sql = "UPDATE clientconnector SET correctmic = %s WHERE uuid = %s"
        val = (mic, uuid)
        mycursor.execute(sql, val)

        mydb.commit()
        cprint.printColor("Mic added to SQL.", "CYAN")
    

#Client connector end.
#==============================

def getRandomGroup():
    if createConnection():
        mycursor = mydb.cursor()
        mycursor.execute("SELECT groupspam FROM groupstospam ORDER BY RAND() LIMIT 1")
        myresult = mycursor.fetchall()
        group = myresult[0][0]
        return group

def getMode():
    if createConnection():
        mycursor = mydb.cursor()
        mycursor.execute("SELECT mode FROM spambotmode ORDER BY time DESC LIMIT 1")
        myresult = mycursor.fetchall()
        mode = myresult[0][0]
        return mode

def getAccount():
    if createConnection():
        mycursor = mydb.cursor()
        mycursor.execute("SELECT username,password FROM robloxaccounts ORDER BY RAND() LIMIT 1")
        myresult = mycursor.fetchall()
        username = myresult[0][0]
        password = myresult[0][1]
        return username, password

def insertMachineLearning(messagessent,captchasuccess):
    if createConnection():
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
    if createConnection():
        mycursor = mydb.cursor()
        mycursor.execute("SELECT groupspam FROM spamgroup ORDER BY time DESC LIMIT 1")
        
        myresult = mycursor.fetchall()[0]
        return myresult[0]

def getRecentMessage():
    if createConnection():
        mycursor = mydb.cursor()
        mycursor.execute("SELECT message FROM spammessage ORDER BY time DESC LIMIT 1")
        
        myresult = mycursor.fetchall()[0]
        return myresult[0]

def insertAccount(username, password):
    if createConnection():
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
    
    print("This is the SQL script running as main!")
