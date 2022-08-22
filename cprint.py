import os
import sys
import time

from colorama import init
from colorama import Fore, Back, Style
init()

#function for printing character by character
def printColor(string,color="RED"):
    if (color == "RED"):
        print(Fore.RED)
        print(string)
        print(Style.RESET_ALL)
    elif (color == "GREEN"):
        print(Fore.GREEN)
        print(string)
        print(Style.RESET_ALL)
    elif (color == "YELLOW"):
        print(Fore.YELLOW)
        print(string)
        print(Style.RESET_ALL)   
    elif (color == "BLUE"):
        print(Fore.BLUE)
        print(string)
        print(Style.RESET_ALL)
    elif (color == "MAGENTA"):
        print(Fore.MAGENTA)
        print(string)
        print(Style.RESET_ALL)
    elif (color == "CYAN"):
        print(Fore.CYAN)
        print(string)
        print(Style.RESET_ALL)

def cprint(input, newline=True, delay1 = 0.01):
    strlen = len(input)
    z = 0
    while 1:
        sys.stdout.flush()
        time.sleep(delay1)
        print(input[z],end='')
        z = z + 1
        if z == strlen:
            if (newline == True):    
                print('\r')
            sys.stdout.flush()
            time.sleep(0.5)
            break

#for clearing console
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)
clearConsole()