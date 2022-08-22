import mysql.connector

global mydb
mydb = mysql.connector.connect(
      host="10.0.0.9",
      user="root",
      password="alexander53",
      database="maindatabase"
    )
    
import datetime 
global now
now = datetime.datetime.now()

def getRandomGroup():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT GROUPSPAM FROM groupstospam ORDER BY RAND() LIMIT 1")
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
    mycursor.execute("SELECT GROUPSPAM FROM spamgroup ORDER BY TIME DESC LIMIT 1")
    
    myresult = mycursor.fetchall()[0]
    return myresult[0]

def getRecentMessage():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT MESSAGE FROM spammessage ORDER BY TIME DESC LIMIT 1")
    
    myresult = mycursor.fetchall()[0]
    return myresult[0]

def insertAccount(username, password):
    mycursor = mydb.cursor()

    #need to include the ` symbole for columns in the table that have a space in their name, apparently
    sql = "INSERT INTO robloxaccounts (USERNAME, PASSWORD, `TIME CREATED`) VALUES (%s, %s, %s)"
    val = (username, password, str(now))
    mycursor.execute(sql, val)
    
    mydb.commit()
    cprint.printColor("Account inserted","CYAN")
    
def getDbSize():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM maintable")
    myresult = mycursor.fetchall()

    db_size = 0;
    for x in myresult:
      db_size += 1
    return db_size
    
def insertIntoDb(num, var, std, mean, median):

    mycursor = mydb.cursor()

    sql = "INSERT INTO crowdtraining (num, var, std, mean, median, time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (num, var, std, mean, median, str(now))
    mycursor.execute(sql, val)

    mydb.commit()
    
    cprint.printColor("Record inserted.","CYAN")
    print("")
    
def Average(lst):
    return sum(lst) / len(lst)
    
import cprint
    
def compareAllDb(var,std,mean,median):
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT var FROM crowdtraining")
    myresult = mycursor.fetchall()
    
    avgPercent = list()
    
    for x in myresult:
      compare = abs(var - float(x[0]))
      avgPercent.append(compare)
    
    print("The average percent difference for var: ")
    cprint.printColor(Average(avgPercent),"YELLOW")
    
    #=================================================
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT std FROM crowdtraining")
    myresult = mycursor.fetchall()
    
    avgPercent2 = list()
    
    for x in myresult:
      compare = abs(std - float(x[0]))
      avgPercent2.append(compare)
    
    print("The average percent difference for std: ")
    cprint.printColor(Average(avgPercent2),"YELLOW")
    
    #=================================================
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT mean FROM crowdtraining")
    myresult = mycursor.fetchall()
    
    avgPercent3 = list()
    
    for x in myresult:
      compare = abs(mean - float(x[0]))
      avgPercent3.append(compare)
    
    print("The average percent difference for mean: ")
    cprint.printColor(Average(avgPercent3),"YELLOW")
    
    #=================================================
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT median FROM crowdtraining")
    myresult = mycursor.fetchall()
    
    avgPercent4 = list()
    
    for x in myresult:
      compare = abs(median - float(x[0]))
      avgPercent4.append(compare)
    
    print("The average percent difference for median: ")
    cprint.printColor(Average(avgPercent4),"YELLOW")
    
    #==================================================
    
    return Average(avgPercent), Average(avgPercent2), Average(avgPercent3), Average(avgPercent4)
    
if __name__ == "__main__":    
    
    print(getMode())
    print(getRandomGroup())
