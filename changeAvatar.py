#Import the main script
import main

#Selenium related imports
global browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

#=========================================
#Global defines

global AVATAR_PANTS 
AVATAR_PANTS =  r"https://www.roblox.com/catalog/382537569/Black-Jeans"
global AVATAR_TOP 
AVATAR_TOP = r"https://www.roblox.com/catalog/607785314/ROBLOX-Jacket"
global AVATAR_HAT
AVATAR_HAT = r"https://www.roblox.com/catalog/607702162/Roblox-Baseball-Cap"

#=========================================
#Function defines

def purchaseClothes():

#=========================================

if __name__ == "__main__":

    print("This is the Avatar changing script running as main!")

    global browser
    browser = main.initSelenium();

    