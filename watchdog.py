from subprocess import Popen
import sys

filename = r"main.py"
while True:
    print("\nStarting " + filename)
    p = Popen("python " + filename, shell=True)
    p.wait()