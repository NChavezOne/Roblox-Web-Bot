import SQLBackup
import os
import time

import pickle
import main
browser = main.initSelenium()
browser.get("https://roblox.com/login")
print(pickle.dumps(browser.get_cookies()))