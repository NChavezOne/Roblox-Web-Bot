import os
import requests

def getLatestCommit():
    r = requests.get("https://github.com/NChavezOne/Roblox-Spam-Bot/commit/main")
    response = str(r.text)
    indexOf = (response.find(r"""class="sha user-select-contain">""") + 32)
    subStr = response[indexOf:len(response)]
    indexOf = (subStr.find(r"<"))
    subStr = subStr[0:indexOf]
    return subStr
    
if __name__ == "__main__":
    
    print(getLatestCommit())