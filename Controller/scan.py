import subprocess
import yaml
import docker
import re
import sys
import os
import json
from common import get_yaml, save_to_file


# def scan_os():
#     # Get path of yml file (from build.py)
#     path = get_yaml()

#     try:
#         # Open yml filr and get host data
#         with open(path, "r") as f:
#             data = yaml.safe_load(f)

#         host_name = []

#         for service in data['services']:
#             try:
#                 scan_host = subprocess.run(
#                     ["docker","exec","-it","scanner","nmap","-O",service], 
#                     capture_output=True, # capture scan results (stdout)
#                     text=True # get results as string
#                 )

#                 if(scan_host.returncode==0):
                    
#                     # Get output of scan
#                     output = scan_host.stdout

#                     os_search = re.search(r"OS details:\s*(.*)", output)

#                     if os_search is None:
#                         print(f"OS information not found for {service}")
#                     else:
#                         os = os_search.group(1)
#                         print(f"[✓]{service} contains the Operating system: {os}")

#                 else:
#                     print("[X] OS scanner process had an error")
#             except:
#                 print("Unexpected error:", sys.exc_info())

#     except Exception as e:
#         print(f"Error opening YAML file: {e}")

def scan_ports():
    path = get_yaml()

    try:
        # Open yml file and get host data
        with open(path, "r") as f:
            data = yaml.safe_load(f)

        host_name = []

        # Get file name of template file - Used in naming results file of a scanned image
        filename = os.path.basename(path)

        

        for service in data['services']:
            if "scanner" not in service:

                # Define path where results of the port scan will be stored
                json_path = os.path.join("./Results/", f"{filename}_{service}.json")

                try:
                    scan_ports = subprocess.run(
                        ["sudo", "docker", "exec", "scanner", "nmap", "-sV", "-oJ", "-", service],
                        capture_output=True, # capture scan results (stdout)
                        text=True # get results as string
                    )

                    if(scan_ports.returncode==0):
                        scan_output = json.loads(scan_ports.stdout)

                        # Write to results.json file of container
                        save_to_file(json_path, scan_output,"w")
                        
                        print(f"[✓] {service}'s ports were scanned successfully")

                    else:
                        print("[X] The port scan was unsuccessful")
                except:
                    print("[X] Unexpected error :", sys.exc_info())
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
            if "scanner" not in service:
                # Get Docker image which will be scanned by Trivy
                image = get_image(service)

                if not image:
                    print(f"[X] No image defined for service: {service}")
                    print(f"Exiting...")
                    sys.exit(1)
                else:
                    
                    # Get file name of template file - Used in naming results file of a scanned image
                    filename = os.path.basename(path)

                    # Define path where results of the Trivy scan will be stored
                    json_path = os.path.join("./Results/", f"{filename}_{service}.json")
                    
                    try:
                        print(f"Scanning {service}'s file system for vulnerabilities...")

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
                            save_to_file(json_path, filtered_results,"w")
                            
                        else:
                            print(f"[X] Error scanning {service} ({image}): {scan_host.stderr}")

                    except Exception as e:
                        print("Unexpected error:", sys.exc_info())

    except Exception as e:
        print(f"Error opening YAML file: {e}")

if __name__ == "__main__":
    scan_ports()
