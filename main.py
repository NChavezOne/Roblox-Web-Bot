#Script for spamming a message into a variety of Roblox Groups.
#Source code modified from DiscordLoginTester.py
#Started 8/2/22
#Version 1 completed 8/15/22

import os
import sys
import time
import random
import string

import pyautogui
pyautogui.FAILSAFE = False #Disable the failesafe, i.e. click in corners

import pyperclip
import keyboard
import mouse

#init colorama
from colorama import init
from colorama import Fore, Back, Style
init()
#selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
#cprint
import cprint
#machine learning
import machinelearning
#client connector
import clientConnector
#client updater
import clientUpdater
#==================
#Moved to top of script
import numpy

import audio #Audio recording script.
import MySQLConnector #MySQLScript.

#==================
#For captchaColor workaround
import PIL.ImageGrab

#==================
#Global defines

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

global unknownErrorRatelimitFlag

def killThreads():
    global stop_threads
    stop_threads = True
    print('thread killed')
    time.sleep(2)

def genRandomString(length = 20):
    N = length
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

def createAccount(username = "TEST", password = "TEST"):
    global userCreated
    global passCreated
    
    print("")
    print("Attempting to create account " + str(username) + " " + str(password))
    
    #pyautogui.moveTo(1792,963) #accept cookies
    #pyautogui.click()
    
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

def goToGroup():
    if (MySQLConnector.getMode() == 0):
        group = MySQLConnector.getRecentGroup()
    elif (MySQLConnector.getMode() == 1):
        group = MySQLConnector.getRandomGroup()
    browser.get(group)
    browser.maximize_window()

def joinGroup():
    print("Attempting to join group.")
    i = 0
    while (isElementPresentByID("group-join-button") != True):
        cprint.printColor("Waiting for join button...","RED")
        browser.refresh()
        time.sleep(2)
        i += 2
        if (i > 6):
            print("No join button, breaking out of function.")
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
    
    print("Sending message!")
    
    #message = "Roblox is a platform that enables the exploitation of young children."
   
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
    
    checkForCaptcha(True)

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
    
    time.sleep(3)
    
    if (isElementPresentByID("FunCaptcha") == True):
        print("FunCaptcha found")
        
        time.sleep(2)
        
        if (isElementPresentByID("fc-iframe-wrap") == True):
            iframe = browser.find_element(By.ID,"fc-iframe-wrap")
            if (len(browser.find_elements("xpath", "//iframe[@id='fc-iframe-wrap']")) > 1):
                print("Duplicate Captchas found. Refreshing page...")
                browser.refresh()
                return False
            print("fc-iframe-wrap found. Changing scope...")
            browser.switch_to.frame(iframe)
        
        if (isElementPresentByID("CaptchaFrame") == True):
            iframe = browser.find_element(By.ID,"CaptchaFrame")
            print("CaptchaFrame found. Changing scope...")
            browser.switch_to.frame(iframe)
        
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
    
    cprint.printColor("Captcha was not detected.","GREEN")
    return False

def openCaptcha():
    browser.switch_to.default_content()
    while (isElementPresentByID("fc-iframe-wrap") != True):
        print("Iframe not found. Trying again...")
        time.sleep(0.5)
    iframe = browser.find_element(By.ID,"fc-iframe-wrap")
    print("fc-iframe-wrap found. Changing scope...")
    browser.switch_to.frame(iframe)
    
    browser.find_element(By.ID, "fc_meta_audio_btn").click()
    time.sleep(1.5)
    
    while (isElementPresentByID("CaptchaFrame") != True):
        print("CaptchaFrame not found. Trying again...")
        time.sleep(0.5)
    iframe = browser.find_element(By.ID,"CaptchaFrame")
    print("CaptchaFrame found. Changing scope...")
    browser.switch_to.frame(iframe)

firstTime = True
captchasuccess = list() #Depracated.

def crackCaptcha(group=False):
    global firstTime
    global Captchas_Encountered
    
    pingClient(our_uuid)
    
    cprint.printColor("Attempting to crack captcha.","YELLOW")
    Captchas_Encountered += 1
    if (Captchas_Encountered >= 10):
        print("More than 10 captchas encountered, getting correct Mic.")
        audio.getCorrectMic()
        print("Restarting script.")
        time.sleep(3)
        Captchas_Encountered = 0
        breakout = (1 / 0)
    print("")
    
    if ((len(browser.find_elements("xpath", "//*[contains(text(), 'Use of the audio challenge for this user has been unusually high. Please try again.')]"))) >= 1):
        print("Roblox ratelimitting us.")
        time.sleep(1)
        breakout = (2 / 0)
    
    time.sleep(5) #give the captcha some time to load.
    
    #Play the audio so we can record it.
    #=======================
    if (group == True):
        pyautogui.moveTo(840,411) #Position of play button
        pyautogui.click()
    elif (group == False):
        pyautogui.moveTo(830,600) #Other possible position
        pyautogui.click()
    #=======================
    
    
    #array to store the audio data in
    audioDataRaw = list()
    
    #Listen for the audio clips
    #====================================
    
    time.sleep(2)
    
    print("Option 1:")
    time.sleep(1.1) #Time for option one TTS
    audioDataRaw.append(audio.recordAudio(int(3)))
    
    print("Option 2:")
    time.sleep(1.1) #Time for option two TTS
    audioDataRaw.append(audio.recordAudio(int(3)))

    print("Option 3:")
    time.sleep(1.1) #Time for option three TTS
    audioDataRaw.append(audio.recordAudio(int(3)))

    #====================================
    print("End of audio gathering.")
    i = 0
    while (i < 3): #Cut all the recorded audio clips.
        audioDataRaw[i] = audioDataRaw[i][int(len(audioDataRaw[i])/10):int(len(audioDataRaw[i])-(len(audioDataRaw[i])/10))] #Cut off the first and last 10% of each audio clip.
        i+=1
    
    #perform audio processing
    #====================================
    
    i = 0
    while (i < 3):
        #print("Raw Audio Data: ")
        #print(i)
        #print(audioDataRaw[i])
        i +=1
    #====================================
    #Create and compare
    
    print("Creating the audio files.")
    i = 0
    while (i < 3):
        file = "option" + str(i+1)
        audio.createFileFromData(r"Audio & Spectrograms/",audioDataRaw[i],file,"wav")
        i +=1
    
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
    
    print("")
   
    if (firstTime == True):
        supervision = False
        #If we are doing supervised machine learning, query the user for the correct audio clip
        #Deprecated.
        if (supervision == True):
            correct_one = input("Which option was the correct audio clip?")
            if (correct_one != 5):
                print("Okay. Adding to SQL, I'll replace what I wrote in the box")
                
                if (correct_one == (myGuess)):
                    captchasuccess.append(1)
                    print("My guess was correct!")
                elif (correct_one != myGuess):
                    captchasuccess.append(0)
                    print("My guess was not correct.")
                
                #MySQLConnector.insertIntoDb(60, float(data_var[int(correct_one)]), float(data_std[int(correct_one)]))
                if (group == True):
                    pyautogui.moveTo(1000,415) #Position of submission box
                    pyautogui.click()
                elif (group == False):
                    pyautogui.moveTo(983,592) #Other possible position
                    pyautogui.click()
            else:
                print("Breaking out.")
            firstTime = True
        else:
            correct_one = myGuess
        
    keyboard.write(str(correct_one))
    time.sleep(1)
    
    global firstCaptcha
    global captchaColor
    #======================================
    if (firstCaptcha == True):
        #For the first globall encountered captcha, set the captchacolor.
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
    
    print("Waiting 3 second...")
    time.sleep(3)
    
    browser.switch_to.default_content()
    if (isElementPresentByID("fc-iframe-wrap") == True):
        print("fc-iframe-wrap still here! Waiting 0.5 second.")
        iframe = browser.find_element(By.ID,"fc-iframe-wrap")
        browser.switch_to.frame(iframe)
        time.sleep(0.5)
        
        if ((len(browser.find_elements("xpath", "//*[contains(text(), 'Use of the audio challenge for this user has been unusually high. Please try again.')]"))) >= 1):
            print("Roblox ratelimitting us.")
            time.sleep(1)
            breakout = (2 / 0)
        
        if ((isElementPresentByID("CaptchaFrame") == True) and (isElementPresentByID("fc_meta_changeback") == True)):
            print("CaptchaFrame and close button found, wait 0.5 seconds.")
            time.sleep(0.5)
            #pyautogui.moveTo(1450,715) #random position
            #pyautogui.click()
            browser.switch_to.default_content()
            if (isElementPresentByID("fc-iframe-wrap") == True):
                iframe = browser.find_element(By.ID,"fc-iframe-wrap")
                browser.switch_to.frame(iframe)
                if (isElementPresentByID("CaptchaFrame") == True):
                    iframe = browser.find_element(By.ID,"CaptchaFrame")
                    browser.switch_to.frame(iframe)
                    
                    if ((len(browser.find_elements("xpath", "//*[contains(text(), 'Use of the audio challenge for this user has been unusually high. Please try again.')]"))) >= 1):
                        print("Roblox ratelimitting us.")
                        time.sleep(1)
                        breakout = (2 / 0)
                    
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
    print("No other captchas found.")
    print("")
    
def isElementPresentByID(what):
    try: browser.find_element(By.ID, what)
    except NoSuchElementException: return False
    return True
    
def isElementPresentByClass(what):
    try: browser.find_element(By.CLASS_NAME, what)
    except NoSuchElementException: return False
    return True

def sendThreeMessages():
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
        
    y = checkMessage()
    messagesSent = y - x

master_delay = 1 #master delay, for various page loading tasks

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
    
global message
global Global_Iterations
global Captchas_Encountered

def pingClient(uuid):
    global our_uuid
    if(True):
        uuid = our_uuid
        client_upd = clientUpdater.getCurrentCommit()
        try:
            MySQLConnector.pingClient(uuid, device_name, git_commit = client_upd[0:5])
            print("Client service pinged.")
        except Exception as ex:
            print(ex)
            print("Error pinging client, try again next cycle.")

global our_uuid
global unknownErrorCount
global stop_threads

if __name__ == "__main__":
    
    #Global defines and setting
    
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
    
    
    #Connect to the client monitoring script, and begin periodic pining
    
    clientConnector.connectToSQLClientService()
    global our_uuid 
    our_uuid = clientConnector.returnUuid()
    
    #Deprecated ping threading, too buggy. Just ping when you solve a captcha
    
    #Get, and then set the proper loopback for captcha audio processing
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
        
    #audio.getCorrectMic()
    
    #Main program loop
    times_executed = 0
    while (times_executed < 10): 
        #uncomment if bypassing try except block
        #if (1 == 1):
        try:
            #cprint.clearConsole()
            
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
            
            #get the message from MySQL
            global message
            message = str(MySQLConnector.getRecentMessage())
            
            global browser
            chromedriver = "chromedriver.exe"
            browser = webdriver.Chrome(executable_path=chromedriver)
            browser.switch_to.window(browser.current_window_handle)
            browser.set_page_load_timeout(30) #We don't want pages that take more than 30 seconds to load.
            browser.maximize_window()
            
            #If we aren't getting ratelimited, create a new account. Otherwise, use on that already exist.
            if (unknownErrorRatelimitFlag == True):
                unknownErrorCount += 1
                if (unknownErrorCount >= 10):
                    print("It's been a while, lets see if we're still getting ratelimited.")
                    unknownErrorCount = 0
                    unknownErrorRateLimitFlag = False
                print("We are getting ratelimited")
                username, password = MySQLConnector.getAccount()
                global userCreated #This isn't actually a recently created account, but we need to
                #Define it as one so the program doesn't break
                userCreated = username
                print("Logging into account - Username: " + str(username) + " Password: " + str(password))
                logIntoAccount(username, password)
                accountJustCreated = False
            else:
                createAccount(genRandomString(),genRandomString())
                time.sleep(master_delay)
                validateAccount()
                accountJustCreated = True
            
            goToGroup()
            time.sleep(master_delay)
            
            #If it's a fresh account, we'll need to go straight to attempting to join the group.
            if (accountJustCreated == True):
                joinGroup()
            
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
            
            MySQLConnector.insertMachineLearning(messagesSent, 1)
            
            accountJustCreated = False
            browser.close()
            Global_Iterations += 1
            print("Waiting 2 seconds...")
            time.sleep(2)
            
            times_executed += 1
        except Exception as ex:
            print(ex)
            print("Either an error was encountered or a breakout occured. Going to start of script...")
            try:
                browser.close()
            except:
                print("Browser close error")
            time.sleep(1)
            
            killThreads()

    print("Script was executed 10 times. Running new program.")
    
    killThreads()

    
    cmd = "main.py"
    os.system(cmd)