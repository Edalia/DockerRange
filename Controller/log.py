import subprocess
from time import gmtime, strftime
import os

def log_event(event):
    
    log_path = "..\Log\logs.txt"

    with open(log_path, "a") as f:
        f.write(strftime("%Y-%m-%d %H:%M:%S", gmtime())+":  "+event+ "\n")

