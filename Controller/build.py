import sys
import subprocess

# Helper functions
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

# Builds container
def build_template():
        path = get_yaml()

        print("Starting...")

        # Build containers /network connections specified by yml file
        build_process = subprocess.Popen(
            ["docker", "compose", "-f", path, "up", "-d", "--build"], 
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