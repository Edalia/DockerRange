from build import get_yaml
import sys
import subprocess
import os
from pathlib import Path
from common import get_file

def tear_senario():
    path = get_yaml()

    print("Tearing down environment...")

    # Tear containers /network connections specified by yml file
    tear_process = subprocess.Popen(
        ["docker", "compose", "-f", path, "down"], 
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in tear_process.stdout:
        print(line, end="")

    # Delay while drop process continues
    tear_process.wait()

    # Retrieve json results files associated with this template (yml file)
    files = get_file(path)
    
    if files is None:
        print("[✓] The environment was torn down successfully, no results file to remove")
        sys.exit(1)

    if(tear_process.returncode == 0):
        for f in files:
             file_path = os.path.join("./Results", f)
             os.remove(file_path)

        print("[✓] The environment was torn down successfully")
    else:
        print("[X] Could not tear down the template") 

if __name__ == "__main__":
    tear_senario()