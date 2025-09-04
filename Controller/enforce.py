import json
import yaml
import time
from common import *

def read_policy():

    policy_file = "./Policy/policy.json"

    with open(policy_file, "r") as f:
        
        policy_data = json.load(f)

        if policy_data:
            return policy_data
        else:
            print("No policies were found")

# def read_results_file(results_file):
#     with open(results_file, "r") as f:
        
#         policy_data = json.load(f)

#         if policy_data:
#             return policy_data
#         else:
#             print("No policies were found")

def get_compliant_hosts():
    path = get_yaml()

    files = get_file(path)
    
    policy = read_policy()

    compliant = []

    # Open read content within each file, each file represents a host
    for f_name in files:
        with open(f"./Results/{f_name}", "r") as f:
            file_data = yaml.safe_load(f)
            
            low = 0
            medium = 0
            high = 0 
            critical = 0

            # for each object in results file, count the number of instances of a severity
            for data in file_data:
                if data.get("Severity") == "LOW":
                    low = low + 1
                elif data.get("Severity") == "MEDIUM":
                    medium = medium + 1
                elif data.get("Severity") == "HIGH":
                    high = medium + 1
                elif data.get("Severity") == "CRITICAL":
                    critical = high + 1

            # If the host has less/equal number of severities than what is allowed, host is compliant
            if(low <= policy['max_low_CVE'] and  medium <= policy['max_medium_CVE'] and high <= policy['max_high_CVE'] and critical <= policy['max_critical_CVE']):
                
                 # Get name of compliant host from file name
                host = f_name.split('_')[-1].split('.')[0]
                log_event(f"{host} complies with the security policy")
                compliant.append(host)
        
    return compliant


def enforce():

    hosts = get_compliant_hosts()
    
    print(f"[!] Retrieving compliant devices...")
    
    time.sleep(2)

    try:

        for host_name in hosts:
            print(f"[...] Modifying devices network settings...")
            disconnect_untrusted = subprocess.run(
                                ["sudo", "docker", "network", "disconnect", "environment_untrusted", host_name],
                                capture_output=True,
                                text=True
                            )
            time.sleep(2)
            if(disconnect_untrusted.returncode == 0):
                print(f"[...] Finalising...")
                connect_trusted = subprocess.run(
                                    ["sudo", "docker", "network", "connect", "environment_trusted", host_name],
                                    capture_output=True,
                                    text=True
                                )
                if(connect_trusted.returncode == 0):
                    print(f"[✓] {host_name} was permitted to join the trusted network")
                    log_event(f"{host_name} has accessed the trusted network")
                else:
                    print(f"[X] {host_name} was not allowed to join the trusted network")
            else:
                print(f"[X] There was an error modifying {host_name}'s network")
    except Exception as e:
        print(f"Error opening YAML file: {e}")

if __name__ == "__main__":
    enforce()