#Script for spamming a message into a variety of Roblox Groups.
#Source code modified from DiscordLoginTester.py
#Started 8/2/22
#Version 1 completed 8/15/22
#Version 2: being worked on in VSCode on 9/2/22

#==============================
#Global generic imports

import os
from os.path import exists
import shutil
import sys
import time
import random
import string
import threading
import signal
import numpy
import PIL.ImageGrab
import datetime

#==============================
#Global imports for pip installs

import pickle #not sure if global or generic
import pyautogui
pyautogui.FAILSAFE = False #Disable the pyautogui failsafe, so it can click in corners
import pyperclip
import keyboard
import mouse
import glob

from colorama import init
from colorama import Fore, Back, Style
init() #Import and initialize colorama
#Selenium related imports
global browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

#==============================
#Imports for personal local scripts
import cprint
import machinelearning
import clientConnector
import clientUpdater
import audio
import MySQLConnector
import changeCookies

#==================
#Global variable defines

global device_name
device_name = os.environ['COMPUTERNAME']

global firstCaptcha
global captchaColor
firstCaptcha = True

global accountJustCreated
global userCreated
global passCreated

global messagesSent
messagesSent = 0

#Some interrupt related stuff for the captcha solver
global captchaHandlerError
global unknownErrorRatelimitFlag
global stopCaptchaFlag
global machineLearnKilled
global recordSKilled
global sendPostFlag

stopCaptchaFlag = True
sendPostFlag = False

global capoptions
captions = list()

global myGuess

global globalGroup

global message
global Global_Iterations
global Captchas_Encountered

global master_delay
master_delay = 1 #master delay, for various page loading tasks

global current_group
global current_group_link

global capcheck

global joinbreaks

global iso_time
iso_time = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")

global backed_up
global last_backup

#========================================
#Operating system related functions

def countFiles(folder):
    count = 0
    dir_path = folder
    for path in os.scandir(dir_path):
        if path.is_file():
            count += 1
    return count

def truncateFolder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def createAccountFolder(dirname):
    directory = dirname
    parent_dir = r"cookies/"
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    return None

def createGroupFolder(account, dirname):
    directory = dirname
    parent_dir = f"cookies/{account}/"
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    return None
#========================================
#Web automation related functions

def initSelenium():
    global browser
    chromedriver = "chromedriver.exe"
    browser = webdriver.Chrome(executable_path=chromedriver)
    browser.switch_to.window(browser.current_window_handle)
    browser.set_page_load_timeout(30) #We don't want pages that take more than 30 seconds to load.
    browser.maximize_window()
    
    pyautogui.moveTo(840,411) #Random position
    pyautogui.click()

def isElementPresentByID(what):
    try: browser.find_element(By.ID, what)
    except NoSuchElementException: return False
    return True
    
def isElementPresentByClass(what):
    try: browser.find_element(By.CLASS_NAME, what)
    except NoSuchElementException: return False
    return True

def waitForElement(method, what, **kwargs):
    timeout = 1
    if (method == "ID"):
        timeout *= 10
        i = 0
        while(isElementPresentByID(what) != True):
            time.sleep(0.1)
            i += 1
            if (i >= timeout):
                break
        if (isElementPresentByID(what) == True):
            return True
        else:
            return False
    elif (method == "Class"):
        timeout *= 10
        i = 0
        while(isElementPresentByClass(what) != True):
            time.sleep(0.1)
            i += 1
            if (i >= timeout):
                break
        if (isElementPresentByClass(what) == True):
            return True
        else:
            return False

def waitForTextInScope(text):
    timeout = 1
    i = 0
    while ((len(browser.find_elements("xpath", f"//*[contains(text(), '{text}')]"))) <= 0):
        time.sleep(0.10)
        i += 1
        if (i >= timeout):
            break

#========================================
#Other Function defines

def infectGroup():
    global unknownErrorRatelimitFlag

    i = countFiles(f"cookies/{our_uuid}/{current_group}")
    while (i < 2):
        global accountJustCreated
        browser.close()
        initSelenium()
        if (unknownErrorRatelimitFlag != True):
            browser.get("https://roblox.com/login")
            createAccount(genRandomString(),genRandomString())
            time.sleep(master_delay)
            validateAccount()
            accountJustCreated = True
        else:
            username, password = MySQLConnector.getAccount()
            logIntoAccount(username,password)
            time.sleep(master_delay)
            accountJustCreated = True
            userCreated = username
            unknownErrorRatelimitFlag = False

        browser.get(current_group_link)
        joinGroup()

        browser.get("https://roblox.com/login")
        time.sleep(1)
        
        path = f"cookies/{our_uuid}/{current_group}/{userCreated}.txt"
        with open(path, 'wb') as filehandler:
            pickle.dump(browser.get_cookies(), filehandler)
        
        print("Account created!")
        time.sleep(1)
        i += 1
    browser.close()
    initSelenium()

def initTensorFlow():
    machinelearning.predictIfCrowd(r"Test Audio/Sample-3s.wav")

def containsTextInScope(text):
    if ((len(browser.find_elements("xpath", f"//*[contains(text(), '{text}')]"))) >= 1):
        return True
    else:
        return False

def genRandomString(length = 20):
    N = length
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

def createAccount(username = "TEST", password = "TEST"):
    global userCreated
    global passCreated
    
    print("")
    print("Attempting to create account " + str(username) + " " + str(password))
    
    #register link for roblox.
    browser.get('https://www.roblox.com/?returnUrl=https%253A%252F%252Fwww.roblox.com%252Fdiscover')
    browser.maximize_window()
    loading_delay = 1 #the delay in seconds to wait for the page to load.
    time.sleep(loading_delay)
    
    listMonths = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    browser.find_element(By.ID, "MonthDropdown").click()
    select = Select(browser.find_element(By.ID, 'MonthDropdown'))
    select.select_by_visible_text(random.choice(listMonths))
    
    i = 0
    listDays = list()
    while (i < 29):
        if (i <= 9):
            listDays.append("0"+str(i))
        else:
            listDays.append(i)
        i += 1
    listDays[0] = "10" #there is no "00" day
    
    browser.find_element(By.ID, "DayDropdown").click()
    select = Select(browser.find_element(By.ID, "DayDropdown"))
    select.select_by_visible_text(str(random.choice(listDays)))
    
    i = 1955
    listYears = list()
    while (i < 2000):
        listYears.append(i)
        i += 1
    
    browser.find_element(By.ID, "YearDropdown").click()
    select = Select(browser.find_element(By.ID, "YearDropdown"))
    select.select_by_visible_text(str(random.choice(listYears)))
    
    user_input = browser.find_element(By.ID, "signup-username")
    user_input.click()
    user_input.send_keys(username)
    
    pass_input = browser.find_element(By.ID, "signup-password")
    pass_input.click()
    pass_input.send_keys(password)
    
    listGenders = [".gender-female",".gender-male"]
    browser.find_element(By.CSS_SELECTOR, random.choice(listGenders)).click()
    
    time.sleep(1)
    pyautogui.moveTo(943,783) #position of logon button
    pyautogui.click()
    
    userCreated = username
    passCreated = password
   
def validateAccount():
    global unknownErrorRatelimitFlag
    while (1):    
        time.sleep(0.25)
        if (isElementPresentByID("signup-usernameInputValidation") == True):
            if (browser.find_element(By.ID, "signup-usernameInputValidation").get_attribute("innerHTML") == "Username not appropriate for Roblox."):
                cprint.printColor("Username not accepted. Trying again", "RED")
                createAccount(genRandomString(),genRandomString())
                continue
            else:
                cprint.printColor("Username was accepted", "GREEN")
                if (isElementPresentByID("GeneralErrorText")):
                    if ((len(browser.find_elements("xpath", "//*[contains(text(), 'unknown error')]"))) >= 1):
                        cprint.printColor("Roblox returns unknown error upon attempted account creation")
                        #If we are getting ratelimited for creating accounts, let's just
                        #Switch to using accounts we've already created.
                        unknownErrorRatelimitFlag = True
                        print("Unknown error ratelimit flag was set.")
                        time.sleep(3)
                        breakout = (1 / 0)
        break
    checkForCaptcha()
    i = 0
    print("Waiting for homepage...")
    while (browser.current_url != "https://www.roblox.com/home"):
        i += 1
        if ( i > 50):
            i = 0
            print("5 seconds has passed with no homepage. Trying again.")
            browser.refresh()
            createAccount(genRandomString(),genRandomString())
            validateAccount()
            checkForCaptcha()
            print("Waiting for homepage...")
        time.sleep(0.1)
    print("Done! Account created successfully!")
    unknownErrorRatelimitFlag = False
    MySQLConnector.insertAccount(userCreated,passCreated)

def goToLogon():
    browser.get(r"https://roblox.com/login")
    browser.maximize_window()

def goToGroup():
    if (MySQLConnector.getMode() == 0):
        group = MySQLConnector.getRecentGroup()
    elif (MySQLConnector.getMode() == 1):
        group = MySQLConnector.getRandomGroup()
    browser.get(group)
    browser.maximize_window()

def getGroupName():
    url = browser.current_url
    substr = url.find(r"#!")
    url = url[0:substr]
    index = 0
    while (True):
        if (url.find("/") == -1):
            break
        index = url.find("/")
        index += 1
        url = url[index:len(url)]
    return url


def joinGroup():
    global joinbreaks
    print("Attempting to join group.")
    i = 0
    while (isElementPresentByID("group-join-button") != True):
        cprint.printColor("Waiting for join button...","RED")
        browser.refresh()
        time.sleep(1)
        i += 1
        if (i > 2):
            print("No join button, breaking out of function.")
            joinBreaks += 1
            return 0
            
    if ((len(browser.find_elements("xpath", "//*[contains(text(), 'Unable to join group.')]"))) >= 1):
        print("We are unable to join the group.")
        time.sleep(1)
        breakout = (2 / 0)
    
    time.sleep(1)
    try:
        browser.find_element(By.ID, "group-join-button").click()
    except:
        cprint.printColor("Couldn't find the join button. Trying with Pyautogui...","RED")
        pyautogui.moveTo(1416,351) #Location of group join button
        pyautogui.click()
    checkForCaptcha(True)
    time.sleep(1)

def sendMessage(message="message"):
    global capcheck
    message = MySQLConnector.getRecentMessage()

    pingClient(our_uuid)
    print("Sending message!")
   
    pyperclip.copy(message)
    while (isElementPresentByID("postData") != True):
        time.sleep(0.1)
        print("Can't find postData. Refreshing page and trying again.")
        browser.refresh()
        time.sleep(1)
        sendMessage()
    
    browser.find_element(By.ID, "postData").click()
    keyboard.send('ctrl+v')
    
    while(isElementPresentByID("postButton") != True):
        time.sleep(0.1)
        print("Can't find postButton. Refreshing page and trying again.")
        browser.refresh()
        time.sleep(1)
        sendMessage()
        
    try:
        browser.find_element(By.ID, "postButton").click()
    except:
        cprint.printColor("Message sent failed.", "RED")
    
    time.sleep(0.5)
    capcheck = False
    if (capcheck != True):
        checkForCaptcha(True)

    if (containsTextInScope("Unable to send post.")):
        print("Roblox says unable to send post.")
        global sendPostFlag
        sendPostFlag = True

def checkMessage():
    cprint.printColor("Checking messages.", "CYAN")
    browser.refresh()
    time.sleep(1)
    global userCreated
    tempString = userCreated[0:4]
    i = len(browser.find_elements("xpath", "//*[contains(text(), '" + tempString +"')]"))
    #print(i)
    return(i)

def checkForCaptcha(group=False):
    cprint.printColor("Checking for Captcha...","YELLOW")
    waittd = 0
    while (True):
        if (isElementPresentByID("FunCaptcha") == True):
            cprint.printColor("FunCaptcha found","CYAN")
            waitForElement("ID","fc-iframe-wrap")
            if (isElementPresentByID("fc-iframe-wrap") == True):
                iframe = browser.find_element(By.ID,"fc-iframe-wrap")
                if (len(browser.find_elements("xpath", "//iframe[@id='fc-iframe-wrap']")) > 1):
                    print("Duplicate Captchas found. Refreshing page...")
                    browser.refresh()
                    return False
                print("fc-iframe-wrap found. Changing scope...")
                browser.switch_to.frame(iframe)
            
            waitForElement("ID","CaptchaFrame")
            if (isElementPresentByID("CaptchaFrame") == True):
                iframe = browser.find_element(By.ID,"CaptchaFrame")
                print("CaptchaFrame found. Changing scope...")
                browser.switch_to.frame(iframe)
                
            print("Waiting for verification...")
            waitForTextInScope("Verification")
            
            waitForElement("ID","home_children_body")
            if (isElementPresentByID("home_children_body") == True):
                if (str(browser.find_element(By.ID,"home_children_body").get_attribute("innerHTML")) == " Please solve this challenge so we know you are a real person"):
                    print("Captcha root found!")
                    openCaptcha()
                    crackCaptcha(group)
                    return True
                else:
                    browser.refresh()
                    print("Captcha root found but InnerHTML Does not match. Refreshing page...")
                    return False
            else:
                browser.refresh()
                print("innterHTML, or IFrame for captcha not found. Refreshing page...")
                return False
        
        time.sleep(0.1)
        waittd += 1
        if (waittd >= 30):
            print("3 seconds has passed without a captcha.")
            break
        
    cprint.printColor("Captcha was not detected.","GREEN")
    return False

def openCaptcha():
    browser.switch_to.default_content()
    while (isElementPresentByID("fc-iframe-wrap") != True):
        print("Iframe not found. Trying again...")
        #time.sleep(0.5)
    iframe = browser.find_element(By.ID,"fc-iframe-wrap")
    print("fc-iframe-wrap found. Changing scope...")
    browser.switch_to.frame(iframe)
    
    browser.find_element(By.ID, "fc_meta_audio_btn").click()
    
    #Try without this sleep. 9/2
    #time.sleep(1.5)
    
    while (isElementPresentByID("CaptchaFrame") != True):
        print("CaptchaFrame not found. Trying again...")
        #time.sleep(0.5)
    iframe = browser.find_element(By.ID,"CaptchaFrame")
    print("CaptchaFrame found. Changing scope...")
    browser.switch_to.frame(iframe)
    
    print("Waiting for Audio Challenge...")
    while ((len(browser.find_elements("xpath", "//*[contains(text(), 'Audio Challenge')]"))) <= 0):
        time.sleep(0.10)
        if (containsTextInScope("Use of the audio challenge for this user has been unusually high. Please try again.")):
            print("Roblox ratelimitting us. Breaking out.")
            time.sleep(1)
            breakout = (2 / 0)
        
    
    print("Audio challenge found!")

def handler(signum, frame):
    print("Crowd cheering found!")
    global stopCaptchaFlag
    global globalGroup
    group = globalGroup
    #Stop playing.
    #=======================
    if (group == True):
        pyautogui.moveTo(840,411) #Position of play button
        pyautogui.click()
    elif (group == False):
        pyautogui.moveTo(830,610) #Other possible position
        pyautogui.click()
    #=======================
    stopCaptchaFlag = True;

def machineLearn():
    global capoptions
    capoptions = list()
    
    global myGuess
    global machineLearnKilled
    global captchaHandlerError

    #==================================================
    #Truncate Folder.
    
    truncateFolder(r"Audio & Spectrograms")
    
    #=================================================
    
    try:
        while (exists(r"Audio & Spectrograms/option1.wav") != True):
            pass
        pred = machinelearning.predictIfCrowd(r"Audio & Spectrograms/option1.wav")
        capoptions.append(pred[0][1])
        
        print(f"PREDICTION: {pred[0][1]}")
        
        thresh = -8
        lower = -13
        
        if (pred[0][1] <= thresh and pred[0][1] > lower):
            myGuess = 1
            signal.raise_signal(signal.SIGTERM)
            machineLearnKilled = True
            return None
        
        while (exists(r"Audio & Spectrograms/option2.wav") != True):
            pass
        pred = machinelearning.predictIfCrowd(r"Audio & Spectrograms/option2.wav")
        capoptions.append(pred[0][1])
        
        print(f"PREDICTION: {pred[0][1]}")
        if (pred[0][1] <= thresh and pred[0][1] > lower):
            myGuess = 2
            signal.raise_signal(signal.SIGTERM)
            machineLearnKilled = True
            return None
        
        while (exists(r"Audio & Spectrograms/option3.wav") != True):
            pass
        pred = machinelearning.predictIfCrowd(r"Audio & Spectrograms/option3.wav")
        capoptions.append(pred[0][1])
        
        print(f"PREDICTION: {pred[0][1]}")
                
        myGuess = capoptions.index(min(capoptions)) + 1
        signal.raise_signal(signal.SIGTERM)
        
        machineLearnKilled = True
    except:
        
        cprint.printColor("Unknown error. Trying with normal method.","RED")
        machineLearnKilled = True
        captchaHandlerError = True
        return None
        
    
#Thread
def recordS():
    #Audio recording thread.
    global stopCaptchaFlag
    global recordSKilled
    
    if (stopCaptchaFlag == False):
        print("Option 1:")
        time.sleep(1.1) #Time for option one TTS
        if (stopCaptchaFlag == False):
            file = "option" + str(1)
            audioDataRaw = audio.recordAudio(3)
            audioDataRaw = audioDataRaw[int(len(audioDataRaw)/10):int(len(audioDataRaw)-(len(audioDataRaw)/10))] #Cut off the first and last 10% of each audio clip.
            audio.createFileFromData(r"Audio & Spectrograms/",audioDataRaw,file,"wav")
    
    if (stopCaptchaFlag == False):
        print("Option 2:")
        time.sleep(1.1) #Time for option Two TTS
        if (stopCaptchaFlag == False):
            file = "option" + str(2)
            audioDataRaw = audio.recordAudio(3)
            audioDataRaw = audioDataRaw[int(len(audioDataRaw)/10):int(len(audioDataRaw)-(len(audioDataRaw)/10))] #Cut off the first and last 10% of each audio clip.
            audio.createFileFromData(r"Audio & Spectrograms/",audioDataRaw,file,"wav")
    
    if (stopCaptchaFlag == False):
        print("Option 3:")
        time.sleep(1.1) #Time for option three TTS
        if (stopCaptchaFlag == False):
            file = "option" + str(3)
            audioDataRaw = audio.recordAudio(3)
            audioDataRaw = audioDataRaw[int(len(audioDataRaw)/10):int(len(audioDataRaw)-(len(audioDataRaw)/10))] #Cut off the first and last 10% of each audio clip.
            audio.createFileFromData(r"Audio & Spectrograms/",audioDataRaw,file,"wav")
            #Done recording audio.
            stopCaptchaFlag = True
    
    recordSKilled = True
    
firstTime = True
captchasuccess = list() #Depracated.

def crackCaptcha(group=False):
    #Global Defines
    global firstTime
    global Captchas_Encountered
    
    global stopCaptchaFlag
    stopCaptchaFlag = False
    
    global myGuess
    
    global globalGroup
    globalGroup = group
    
    #Interrupts
    global machineLearnKilled
    machineLearnKilled = False
    global recordSKilled
    recordSKilled = False
    
    #Interrupt flags
    global captchaHandlerError
    captchaHandlerError = False 
    
    cprint.printColor("Attempting to crack captcha.","YELLOW")
    print("")
    Captchas_Encountered += 1
    if (Captchas_Encountered >= 100):
        print("More than 100 captchas encountered, breaking out.")
        Captchas_Encountered = 0
        breakout = (2 / 0)
    
    if (containsTextInScope("Use of the audio challenge for this user has been unusually high. Please try again.")):
        print("Roblox ratelimitting us. Breaking out.")
        time.sleep(1)
        breakout = (2 / 0)
    
    #Play the audio so we can record it.
    #=======================
    if (group == True):
        pyautogui.moveTo(840,411) #Position of play button
        pyautogui.click()
    elif (group == False):
        pyautogui.moveTo(830,610) #Other possible position
        pyautogui.click()
    #=======================

    #array to store the audio data in
    audioDataRaw = list()
    
    #Listen for the audio clips
    #====================================
    global capoptions
    signal.signal(signal.SIGTERM, handler) #Setup interrupts.
    
    time.sleep(2)
    
    audioService = threading.Thread(target = machineLearn, args = ())
    audioService.start()
    
    recordService = threading.Thread(target = recordS, args = ())
    recordService.start()
    
    #====================================
    
    while(1):
        time.sleep(0.25)
        if(stopCaptchaFlag == True):
            break
    while(1):    
        time.sleep(0.25)
        if (machineLearnKilled == True and recordSKilled == True):
            break
    
    #======================================
    #Execute only if there's an error with the threader
    
    if (captchaHandlerError == True):
        print("These are the machine learning results.")
        options = list()
        options.append(machinelearning.predictIfCrowd(r"Audio & Spectrograms/option1.wav"))
        options.append(machinelearning.predictIfCrowd(r"Audio & Spectrograms/option2.wav"))
        options.append(machinelearning.predictIfCrowd(r"Audio & Spectrograms/option3.wav"))
        
        i = 0
        while (i<3):
            options[i]=options[i][0][1]
            i+=1
        
        myGuess = options.index(min(options)) + 1
        
    
    
    print("My guess for the crowd cheering is " + str(myGuess))
    print("") 

    #====================================
    
    #Go to the submission box.
    #=======================
    if (group == True):
        pyautogui.moveTo(1000,415) #Position of submission box
        pyautogui.click()
    elif (group == False):
        pyautogui.moveTo(983,592) #Other possible position
        pyautogui.click()
    #=======================
    
    correct_one = myGuess  
        
    keyboard.write(str(correct_one))
    time.sleep(1)
    
    global firstCaptcha
    global captchaColor
    #======================================
    if (firstCaptcha == True):
        #For the first globally encountered captcha, set the captchacolor.
        if (group == True):
            x ,y = 990, 461 #For joining groups
        if (group == False):
            x, y = 1008, 640 #For logging in and creating accouts
        captchaColor = PIL.ImageGrab.grab().load()[x,y]
        cprint.printColor("The captchaColor is: "+str(captchaColor),"MAGENTA")
        firstCaptcha = False
    #======================================
    
    if (group == True):
        pyautogui.moveTo(1000,415) #position of submit
        pyautogui.click()
    elif (group == False):
        pyautogui.moveTo(983,592) #possible position aswell
        pyautogui.click()
    
    print("Pressing Enter...")
    keyboard.send('enter')
    
    print("Waiting 0.5 second...")
    time.sleep(0.5)
    
    browser.switch_to.default_content()
    try:
        if (isElementPresentByID("fc-iframe-wrap") == True):
            print("fc-iframe-wrap still here! Waiting 0.5 second.")
            iframe = browser.find_element(By.ID,"fc-iframe-wrap")
            browser.switch_to.frame(iframe)
            #time.sleep(0.5)
            
            if (containsTextInScope("Use of the audio challenge for this user has been unusually high. Please try again.")):
                print("Roblox ratelimitting us.")
                time.sleep(1)
                breakout = (2 / 0)

            if ((isElementPresentByID("CaptchaFrame") == True) and (isElementPresentByID("fc_meta_changeback") == True)):
                print("CaptchaFrame and close button found, wait 0.5 seconds.")

                browser.switch_to.default_content()
                if (isElementPresentByID("fc-iframe-wrap") == True):
                    iframe = browser.find_element(By.ID,"fc-iframe-wrap")
                    browser.switch_to.frame(iframe)
                    if (isElementPresentByID("CaptchaFrame") == True):
                        iframe = browser.find_element(By.ID,"CaptchaFrame")
                        browser.switch_to.frame(iframe)

                        time.sleep(1)

                        while (containsTextInScope("Working, please wait")):
                            print("Loading...")
                        if (containsTextInScope("Use of the audio challenge for this user has been unusually high. Please try again.")):
                            print("Roblox ratelimitting us.")
                            time.sleep(1)
                            breakout = (2 / 0)

                        #Ping client service to let them know we're alvie.
                        pingClient(our_uuid)

                        #So this is a strange workaround. I couldn't figure out how to reliably
                        #Detect duplicate captchas or if roblox throws more captchas, so
                        #I actually just read the color value of one of the pixels on screen and
                        #Check if it matches the color of the submit button lol
                        
                        #Modifying this workaround to make it more portable: instead of comparing
                        #against a preset captchacolor, define the captcha color as encountered on
                        #the first captcha.
                        if (group == True):
                            x ,y = 990, 461 #For joining groups
                        if (group == False):
                            x, y = 1008, 640 #For logging in and creating accouts
                        rgb = PIL.ImageGrab.grab().load()[x,y]
                        if (rgb == captchaColor):
                            print("Captcha Color matches!")
                            print("double checked, crack captcha")
                            crackCaptcha(group)
                        else:
                            print("Captcha Color doesn't match.")
                            time.sleep(1)
                    print("Error, couldn't find captchaframe.")
                print("Error, couldn't find fc-iframe again.")
    except:
        print("Captcha checking error")
        print("No other captchas found.")
        print("")

    #Ping client service to let them know we're alvie.
    pingClient(our_uuid)


def sendThreeMessages():
    global sendPostFlag
    global message
    global messagesSent
    x = checkMessage()
    i = 0
    
    print("Scrolling page...")
    z = 0        
    while (z < 6):
        mouse.wheel(-1)
        z += 1
    
    while (i < 3):
        send_message = message
        time.sleep(0.5)
        sendMessage(send_message)
        i += 1
        if (sendPostFlag == True):
            break
        
    y = checkMessage()
    messagesSent = y - x

def Average(lst):
    return sum(lst) / len(lst)

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
    checkForCaptcha()
    i = 0
    while (browser.current_url != "https://www.roblox.com/home"):
        i += 1
        if ( i > 50):
            i = 0
            print("5 seconds has passed with no homepage. Trying again.")
            browser.refresh()
            logIntoAccount(username, password)
        time.sleep(0.1)
    print("Done! Logged into account.")
    
def pingClient(uuid):
    global our_uuid
    global backed_up
    if(True):
        uuid = our_uuid
        client_upd = clientUpdater.getCurrentCommit()
        try:
            if (MySQLConnector.pingClient(uuid, device_name, git_commit = client_upd[0:5]) == False):
                clientConnector.connectToSQLClientService()
            print("Client service pinged.")

            if (clientConnector.get_ip_address == "10.0.0.9"): #If we are the server
                print("We are the server.")
                last_backup = (datetime.datetime.now().isoformat(sep=" ", timespec="seconds")) - backed_up
                if (last_backup >= 60):
                    backed_up = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
                    os.chdir(r"C:\xampp\mysql\bin")
                    time.sleep(0.5)
                    SQLBackup.createConnection()
                    time.sleep(0.5)
                    os.chdir(r"C:\Users\Admin\Desktop\Main")
                else:
                    print(f"last backup:{last_backup}")
            else:
                print("We are not the server.")

        except Exception as ex:
            print(ex)
            print("Error pinging client, try again next cycle.")

global our_uuid
global unknownErrorCount
global stop_threads

if __name__ == "__main__":
    
    #Global defines and setting
    
    global userCreated 

    global Global_Iterations
    global Captchas_Encountered
    global accountJustCreated
    global unknownErrorRatelimitFlag
    global unknownErrorCount
    unknownErrorCount = 0
    unknownErrorRatelimitFlag = False
    accountJustCreated = False
    Global_Iterations = 1
    Captchas_Encountered = 0
    
    global current_group
    global current_group_link

    global capcheck
    capcheck = True

    global backed_up
    backed_up = (datetime.datetime.now().isoformat(sep=" ", timespec="seconds"))

    #Connect to the client monitoring script, and begin periodic pining
    
    clientConnector.connectToSQLClientService()
    global our_uuid 
    our_uuid = clientConnector.returnUuid()

    #=================================

    #Initialize tensorflow
    initTensorFlow()

    #Get, and then set the proper loopback for captcha audio processing
    #Don't use SQL for now. Doesn't work properly
    TrustSQL = False
    if (TrustSQL):
        the_mic = MySQLConnector.checkIfSameMic(our_uuid)
        cprint.printColor(the_mic)
        if (the_mic == False or the_mic == 0):
            audio.getCorrectMic()
        else:
            audio.setMic(int(the_mic))
            if (audio.isMicWorking()):
                pass
            else:
                audio.getCorrectMic()
                
    audio.getCorrectMic()
    #audio.setMic(3)
    
    #=================================
    #Truncate the cookies folder.

    #truncateFolder(r"cookies")

    #=================================
    #Navigate to our cookie folder
    folder = r"cookies/"
    if (not exists(folder + our_uuid)):
        createAccountFolder(our_uuid)

    #Main program loop
    times_executed = 0
    while (times_executed < 10): 
        #uncomment if bypassing try except block
        #if (1 == 1):
        try:
            
            #First, pull the latest version of the software from git
            if (clientUpdater.upDateIfPossible()):
                os.system("git reset --hard HEAD")
                os.system("git pull origin main")
                stop_threads = True
                print('thread killed')
                time.sleep(2)
                os.system("main.py")
                sys.exit()
            
            #Get the mode we are operating in.
            global mode_operating
            mode_operating = MySQLConnector.getMode()
            cprint.cprint("The mode we are operating in is: " + str(mode_operating))
            time.sleep(1)
            
            Captchas_Encountered = 0
            cprint.printColor("Captchas encountered so far: " + str(Captchas_Encountered))
            time.sleep(1)
            
            #Get the message from MySQL
            global message
            message = str(MySQLConnector.getRecentMessage())
            
            #Initialize selenium
    
            initSelenium()

            goToGroup()
            print("Going to group.")

            current_group = getGroupName()
            current_group_link = browser.current_url
            if (not exists(f"cookies/{our_uuid}/{current_group}")):
                uuid = our_uuid
                createGroupFolder(our_uuid, current_group)

            if (countFiles(f"cookies/{our_uuid}/{current_group}") < 2): #If we have less than 5 cookies
                #If we aren't getting ratelimited, create a new account. Otherwise, use on that already exist.
                infectGroup()
            else:
                #Otherwise, use cookies.
                try:
                    files = f"cookies/{our_uuid}/{current_group}/"
                    files2 = "*.txt"
                    files3 = files + files2
                    accountcookies = glob.glob(files3)
                    try: userCreated
                    except NameError: userCreated = "a"
                    while True:
                        if (len(userCreated) > 1):
                            toCheck = random.choice(accountcookies)
                            flen = len(files)
                            toTest = toCheck[flen:(len(toCheck) - 4)]
                            if (toTest != userCreated):
                                changeCookies.load_cookie(browser, toCheck)
                                userCreated = toTest
                                time.sleep(1)
                                browser.refresh()
                                print(f"Logged into account {userCreated}")
                                break
                        else:
                            toCheck = random.choice(accountcookies)
                            flen = len(files)
                            toTest = toCheck[flen:(len(toCheck) - 4)]
                            changeCookies.load_cookie(browser, toCheck)
                            userCreated = toTest
                            time.sleep(1)
                            browser.refresh()
                            print(f"Logged into account {userCreated}")
                            break
                        capcheck = False
                except Exception as ex:
                    print(f"Couldn't load cookies. Here's the error message: {ex}")

            browser.get(current_group_link)
            time.sleep(master_delay)
            
            #If it's a fresh account, we'll need to go straight to attempting to join the group.
            
            global joinbreaks
            joinbreaks = 0
            print("Waiting for post button...")
            i = 0
            while(1):
                time.sleep(1)
                i += 1
                time.sleep(0.5)
                if (isElementPresentByID("postButton") == True):
                    break
                elif (i > 5):
                    print("No postbutton. Try to join group again...")
                    joinGroup()
                    i = 0
                if (joinbreaks >= 2):
                    print("Joinbreak")
                    breakout = (2 / 0)
            
            while(1):
                if (isElementPresentByID("postButton") == True):
                    sendThreeMessages()
                    break
                else:
                    print("Text input not found. Resetting page.")
                    browser.refresh()
                    print("Page was refreshed.")
                time.sleep(master_delay)
            
            tempstring = "Program over. You have sent " + str(messagesSent) + " message(s)"
            
            print (tempstring)
            MySQLConnector.insertMachineLearning(messagesSent, 1)
            
            accountJustCreated = False
            browser.close()
            Global_Iterations += 1
            print("Waiting 2 seconds...")
            time.sleep(2)
            
            times_executed += 1
            capcheck = True
        except Exception as ex:
            print(ex)
            print("Either an error was encountered or a breakout occured. Going to start of script...")
            try:
                browser.close()
            except:
                print("Browser close error")
            time.sleep(1)
            

    print("Script was executed 10 times. Running new program.")
    cmd = "py main.py"
    os.system(cmd)