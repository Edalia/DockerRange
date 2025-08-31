import subprocess


def scan(device_ip):
result = subprocess.run(['nmap', '-sV', '172.21.0.10'], 
                       capture_output=True, text=True)
print(result.stdout)