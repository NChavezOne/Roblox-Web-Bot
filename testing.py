import SQLBackup
import os
import time

print("Attempting to backup SQL database.")
os.chdir(r"C:\xampp\mysql\bin")
time.sleep(0.5)
SQLBackup.createConnection()
time.sleep(0.5)
os.chdir(r"C:\Users\Admin\Desktop\Main")