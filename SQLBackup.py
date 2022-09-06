#This script is meant to be run on the server.
#It's purpose if to replace the SQL database if it somehow gets deleted.
#The secondary function is to update the origin time and truncate certain tables when a client first connects.
#=========================
#Imports.

import pyautogui
import mysql.connector
import datetime
import time
import cprint

import keyboard

import os

import threading

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

global last_time

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
        #=======================
        
        global last_time
        
        mycursor = mydb.cursor()
        sql = "SELECT origin FROM databaseinfo"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        if (len(myresult) >= 1):
            
            last_time = myresult[0]
            
            mycursor = mydb.cursor()
            sql = "UPDATE databaseinfo SET backup = %s"
            iso_time = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
            val = (iso_time,)
            mycursor.execute(sql,val)
            mydb.commit()
        
        #=======================
        #Backup the SQL database
        backupservice = threading.Thread(target=(backupDatabase),args=(),daemon=True)
        backupservice.start()
        os.system(f"mysqldump -u root -p maindatabase > backup.sql")
        time.sleep(3)
        cprint.printColor("Connection successful. Backed up SQL database.","GREEN")
        #=======================
        return True
    except Exception as e:
        time.sleep(1)
        cprint.printColor("Failed connecting to SQL. Creating new database...","RED")
        print(e)
        time.sleep(5)
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
            cprint.printColor("No database found. Time to create a new one.","RED")
            sqlservice = threading.Thread(target=(createDatabase),args=(),daemon=True)
            sqlservice.start()
            os.system(f"mysql -u {sql_username} -p")
            
            time.sleep(3)
            
            cprint.printColor("Done. Database restored to latest backup.","GREEN")
        else:
            cprint.printColor("Could not connect to maindatabase, however it does exist","RED")
        
        return False

def grantAdminPerms(ips):
    for x in ips:
        keyboard.write(f"GRANT ALL ON maindatabase to root@'{x}' IDENTIFIED BY 'poopoocaca51';")
        time.sleep(0.5)
        keyboard.send('enter')
        time.sleep(1)

def createDatabase():
    #Create the database, set the source as a file called backup.sql in the same directory
    time.sleep(2)
    
    keyboard.write(f"{sql_password}")
    time.sleep(0.5)
    keyboard.send('enter')
    time.sleep(0.5)
    
    keyboard.write(r"CREATE DATABASE maindatabase;")
    time.sleep(0.5)
    keyboard.send('enter')
    time.sleep(0.5)
    
    keyboard.write(r"USE maindatabase;")
    time.sleep(0.5)
    keyboard.send('enter')
    time.sleep(0.5)
    
    keyboard.write(r"SOURCE backup.sql")
    time.sleep(0.5)
    keyboard.send('enter')
    time.sleep(0.5)
    
    time.sleep(5)
    
    #Grant admin perms for the host
    keyboard.write(r"GRANT ALL ON maindatabase to root@'10.0.0.9' IDENTIFIED BY 'poopoocaca51';")
    time.sleep(0.5)
    keyboard.send('enter')
    time.sleep(1)
    
    #Grant admin perms for all others
    ipaddresses = list()
    
    mydb = mysql.connector.connect(
          host=main_host,
          user=sql_username,
          password=sql_password,
          database="maindatabase"
        )
    
    mycursor = mydb.cursor()
    sql = "SELECT internalip FROM clientconnector"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if (len(myresult) >= 1):
        for x in myresult:
            ipaddresses.append(x[0])
            
    grantAdminPerms(ipaddresses)
    time.sleep(1)
    
    clearTables()
    time.sleep(1)
    
    keyboard.write(r"quit")
    time.sleep(0.5)
    keyboard.send('enter')
    time.sleep(0.5)
    
def clearTables():
    mydb = mysql.connector.connect(
          host=main_host,
          user=sql_username,
          password=sql_password,
          database="maindatabase"
        )
    mycursor = mydb.cursor()
    sql = "TRUNCATE TABLE machinelearning"
    mycursor.execute(sql)
    mydb.commit()
    
    keyboard.write(r"CREATE TABLE IF NOT EXISTS `maindatabase`.`databaseinfo` (`origin` TEXT NOT NULL , `backup` TEXT NOT NULL ) ENGINE = InnoDB;")
    time.sleep(0.5)
    keyboard.send('enter')
    time.sleep(1)
    
    mycursor = mydb.cursor()
    sql = "TRUNCATE TABLE databaseinfo"
    mycursor.execute(sql)
    mydb.commit()
    
    mycursor = mydb.cursor()
    sql = "INSERT INTO databaseinfo (origin,backup) VALUES (%s, %s)"
    
    global last_time
    last_time = iso_time
    
    val = (last_time, last_time)
    mycursor.execute(sql,val)
    mydb.commit()
    
    

def backupDatabase():
    #Backup the database into a file called backup.sql in the same directory.
    
    time.sleep(2)
    time.sleep(0.1)
    pyautogui.moveTo(943,783) #position of logon button
    pyautogui.click()
                
    time.sleep(0.1)
    pyautogui.moveTo(152,243) #position of cmd
    pyautogui.click()
    time.sleep(0.1)
    
    os.system(f"{sql_password}")
    time.sleep(0.5)
    keyboard.send('enter')
    time.sleep(0.5)
    
global master_delay

master_delay = 30;
    
if __name__ == "__main__":  
	
    print("This is the SQL backup script running as main!")
    
    while True:
        createConnection()
        time.sleep(master_delay)