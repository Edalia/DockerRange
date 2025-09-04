import subprocess
from time import gmtime, strftime
import os
import sys
import json

def log_event(event):
    
    log_path = "./Log/logs.txt"

    with open(log_path, "a") as f:
        f.write(strftime("%Y-%m-%d %H:%M:%S", gmtime())+":  "+event+ "\n")

# Checks if template provided is valid
def get_yaml():
    if len(sys.argv) == 2:
        # Gets the file path from the argument
        path = sys.argv[1]
        
        if(path.endswith(".yaml") or path.endswith(".yml")):
           return path
        else:
            print("[X] Expecting a .yaml>/ .yml file")
            sys.exit(1)
    else:
        print("[X] Usage: python3 build.py <file.yaml>/ <file.yml>")
        sys.exit(1)

# Retrieve json results files associated with a path (yml file)
def get_file(path):

    filename = os.path.basename(path)

    files = []

    for f in os.listdir("./Results"):
        if filename in f:
            files.append(f)
    
    return files

# Save content to file. @write: a - append, w - write new
def save_to_file(filename, content, write):
    try:
        with open(filename, write) as f:
            json.dump(content, f, indent=2)
        print(f"[✓] Output written to {filename}")
    except Exception as e:
        print(f"[X] Error writing to file {filename}: {e}")