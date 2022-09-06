import SQLBackup
import os
import time

import pickle
import main
import pyautogui
print("Attempting to backup SQL database.")
            
time.sleep(0.1)
pyautogui.moveTo(943,783) #position of logon button
pyautogui.click()
time.sleep(0.1)
pyautogui.moveTo(152,243) #position of cmd
pyautogui.click()
time.sleep(0.1)