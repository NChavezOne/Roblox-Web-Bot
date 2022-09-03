#======================================
#Imports.

import time
import pickle

#Selenium Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

#Import SQL Script
import MySQLConnector

#======================================
#Global defines

global browser #Selenium browser object

#======================================
#Functions.

def initSelenium():
    global browser
    chromedriver = "chromedriver.exe"
    browser = webdriver.Chrome(executable_path=chromedriver)
    browser.switch_to.window(browser.current_window_handle)
    browser.set_page_load_timeout(30) #We don't want pages that take more than 30 seconds to load.
    browser.maximize_window()
    
def goToGroup():
    if (MySQLConnector.getMode() == 0):
        group = MySQLConnector.getRecentGroup()
    elif (MySQLConnector.getMode() == 1):
        group = MySQLConnector.getRandomGroup()
    browser.get(group)
    browser.maximize_window()
    
def logIntoAccount(username, password):
    browser.get("https://www.roblox.com/login")
    browser.switch_to.window(browser.current_window_handle)
    browser.maximize_window()
    print("Logging into account. Username: " + str(username) + " Password: " + str(password))
    browser.find_element(By.ID, "login-username").click()
    browser.find_element(By.ID, "login-username").send_keys(username)
    browser.find_element(By.ID, "login-password").click()
    browser.find_element(By.ID, "login-password").send_keys(password)
    time.sleep(0.5)
    browser.find_element(By.ID, "login-button").click()
    print("Waiting for homepage...")
    #checkForCaptcha()
    i = 0
    while (browser.current_url != "https://www.roblox.com/home"):
        i += 1
        if ( i > 500):
            i = 0
            print("50 seconds has passed with no homepage. Trying again.")
            browser.refresh()
            logIntoAccount(username, password)
        time.sleep(0.1)
    print("Done! Logged into account.")
    
def save_cookie(driver, path):
    path = r"cookies/" + path
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookie(driver, path):
     with open(path, 'rb') as cookiesfile:
         cookies = pickle.load(cookiesfile)
         for cookie in cookies:
            driver.add_cookie(cookie)
             
def saveAccountCookie(browser, username):
    file = f"{username}.txt"
    save_cookie(browser, file)
             
def loadAccountCookie(browser, username):
    file = f"{username}.txt"
    load_cookie(browser, file)
    
#======================================

tokens = ["d","d"]

if __name__ == "__main__":
    
    global browser
    chromedriver = "chromedriver.exe"
    browser = webdriver.Chrome(executable_path=chromedriver)
    browser.switch_to.window(browser.current_window_handle)
    browser.set_page_load_timeout(30) #We don't want pages that take more than 30 seconds to load.
    browser.maximize_window()
    
    print("This is the cookies script running as main!")
    
    while True:
        username = input("input username!")
        saveAccountCookie(browser, username)