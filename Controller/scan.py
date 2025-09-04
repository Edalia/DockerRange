import subprocess
import yaml
import docker
import re
import sys
import os
import json
from build import get_yaml

def scan_os():
    # Get path of yml file (from build.py)
    path = get_yaml()

    try:
        # Open yml filr and get host data
        with open(path, "r") as f:
            data = yaml.safe_load(f)

        host_name = []

        for service in data['services']:
            try:
                scan_host = subprocess.run(
                    ["docker","exec","-it","scanner","nmap","-O",service], 
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

def scan_services():
    path = get_yaml()

    try:
        # Open yml file and get host data
        with open(path, "r") as f:
            data = yaml.safe_load(f)

        host_name = []

        for service in data['services']:
            try:
                scan_apps = subprocess.run(
                    ["docker","exec","-it","scanner","nmap","-sV",service], 
                    capture_output=True, # capture scan results (stdout)
                    text=True # get results as string
                )

                if(scan_apps.returncode==0):
                    output = scan_apps.stdout

                    # Capture "PORT STATE SERVICE VERSION"
                    matches = re.findall(r"(\d+/tcp)\s+open\s+(\S+)\s+(.*)", output)

                    if not matches: # if the output is empty
                        print(f"[X] No identifiable services found on {service}")
                    else:
                        print(f"[✓]{service} running the applications:")
                        for match in matches:
                            port, svc, version = match
                            print(f"[-]{version}, at Port: {port}")
                else:
                    print("[X] Could not return the result")
            except:
                print("[X] Unexpected error scanning hosts:", sys.exc_info())
    except:
        print("[X] Unexpected error parsing template file:", sys.exc_info())

# Used for Trivy scan which needs container image
def get_image(host):
    # connect to Docker
    client = docker.from_env()

    # get a container by name
    container = client.containers.get(host)

    # get the image reference
    image = container.image.tags[0] if container.image.tags else container.image.id

    return image

def trivy_scan():
    path = get_yaml()

    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f)

        for service in data['services']:

            # Get Docker image which will be scanned by Trivy
            image = get_image(service)

            if not image:
                print(f"[!] No image defined for service: {service}")
                print(f"Exiting...")
                sys.exit(1)
            else:
                
                # Get file name of template file - Used in naming results file of a scanned image
                filename = os.path.basename(path)

                # Define path where results of the Trivy scan will be stored
                json_path = os.path.join("./Results/", f"{filename}_{service}.json")
            
                try:
                    scan_host = subprocess.run(
                        ["trivy", "image", "-f", "json", image],
                        capture_output=True,
                        text=True
                    )

                    if scan_host.returncode == 0:
                        
                        # Parse Trivy output stored in json format
                        scan_output = json.loads(scan_host.stdout)

                        # List that stores filtered results. Saved for analysis
                        filtered_results = []
                        
                        # Get vulnerability info from parsed Trivy output
                        for result in scan_output.get("Results", []):
                            for vuln in result.get("Vulnerabilities", []):
                                filtered_results.append(# add CVE and severity to filtered results list
                                    {
                                    "Target": result.get("Target"),
                                    "CVE": vuln.get("VulnerabilityID"),
                                    "Severity": vuln.get("Severity")
                                    }
                                )

                        # Write to results.json file of container
                        save_to_file(json_path, filtered_results)
                        
                    else:
                        print(f"[X] Error scanning {service} ({image}): {scan_host.stderr}")

                except Exception as e:
                    print("Unexpected error:", sys.exc_info())

    except Exception as e:
        print(f"Error opening YAML file: {e}")

def save_to_file(filename, content):
    try:
        with open(filename, "w") as f:
            json.dump(content, f, indent=2)
        print(f"[✓] Output written to {filename}")
    except Exception as e:
        print(f"[X] Error writing to file {filename}: {e}")

if __name__ == "__main__":
    trivy_scan()
