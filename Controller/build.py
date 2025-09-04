import subprocess
from common import get_yaml

# Builds container
def build_template():
        path = get_yaml()

        print("Starting...")

        # Build containers /network connections specified by yml file
        build_process = subprocess.Popen(
            ["docker", "compose", "-f", path, "up", "-d", "--build","--remove-orphans"], 
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in build_process.stdout:
            print(line, end="")

        # Delay while build process continues
        build_process.wait()

        if(build_process.returncode == 0):
            print("[✓] The environment was created successfully")
        else:
           print("[X] Could not build the template") 

if __name__ == "__main__":
    build_template()