#=========================
#Imports.

import mysql.connector
import datetime
import cprint

#========================= 

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

global clientCreated
clientCreated = True;

def createNewClient(uuid, ipaddress, internalip):
    mycursor = mydb.cursor()

    sql = "INSERT INTO clientconnector (uuid, timecreated, lastpinged, status, ipaddress, internalip) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (uuid, str(now), str(now), str(0), ipaddress, internalip)
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
    
def pingClient(uuid):
    mycursor = mydb.cursor()

    sql = "UPDATE clientconnector SET lastpinged = %s WHERE uuid = %s"
    val = (str(now), uuid)
    mycursor.execute(sql, val)

    mydb.commit()

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
    mycursor.execute("SELECT * FROM robloxaccounts ORDER BY RAND() LIMIT 1")
    myresult = mycursor.fetchall()
    username = myresult[0][1]
    password = myresult[0][2]
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
