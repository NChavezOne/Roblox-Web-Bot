import os
import sys
import requests
import threading
import time
import git

def getLatestCommit():
    r = requests.get("https://github.com/NChavezOne/Roblox-Spam-Bot/commit/main")
    response = str(r.text)
    indexOf = (response.find(r"""class="sha user-select-contain">""") + 32)
    subStr = response[indexOf:len(response)]
    indexOf = (subStr.find(r"<"))
    subStr = subStr[0:indexOf]
    return subStr
    
def getCurrentCommit():
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    return sha
    
def updateRepo():
    os.system("git reset --hard HEAD")
    os.system("git pull origin main")
    os.system("main.py")
    sys.exit()
    
def upDateIfPossible():
    if (str(getCurrentCommit()) != str(getLatestCommit())):
        return True
    else:
        #print("We are on the latest version.")
        time.sleep(0.5)
        return False
    
def upDate():
    while(1):
        upDateIfPossible()
    
if __name__ == "__main__":
    
    #clientservice = threading.Thread(target=(upDate),args=(),daemon=True)
    #clientservice.start()
    
    while (1):
        upDateIfPossible()
        i = 0
        while (i < 20):
            print("we should not be here")
            time.sleep(1)
            i += 1