import subprocess
import yaml
import docker
import re
import sys
from build import get_yaml

def scan():
    # Get path of yml file (from build.py)
    path = get_yaml()

    try:
        # Open yml filr and get host data
        with open(path, "r") as f:
            data = yaml.safe_load(f)

        host_name = []

        for service in data['services']:
            if "scanner" not in service:
                try:
                    scan_host = subprocess.run(
                        ["docker","exec","-i","scanner","nmap","-O",service], 
                        capture_output=True, # capture scan results (stdout)
                        text=True # get results as string
                    )

                    if(scan_host.returncode==0):
                        
                        # Get output of scan
                        output = scan_host.stdout

                        os_search = re.search(r"OS details:\s*(.*)", output)

                        if os_search is None:
                            print(f"OS information not found for {service}")
                        else:
                            os = os_search.group(1)
                            print(f"[✓]{service} contains the Operating system: {os}")

                    else:
                        print("[X] OS scanner process had an error")
                except:
                    print("Unexpected error:", sys.exc_info())

    except Exception as e:
        print(f"Error opening YAML file: {e}")


if __name__ == "__main__":
    scan()