import json
from common import get_yaml, save_to_file

def read_policy():

    policy_file = "./Policy/policy.json"

    with open(policy_file, "r") as f:
        
        policy_data = json.load(f)

        if policy_data:
            return policy_data
        else:
            print("No policies were found")

def read_results_file(results_file):
    with open(results_file, "r") as f:
        
        policy_data = json.load(f)

        if policy_data:
            return policy_data
        else:
            print("No policies were found")

def enforce():
    path = get_yaml()

    files = get_file(path)

    for

if __name__ == "__main__":
    enforce()