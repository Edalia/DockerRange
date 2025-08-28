import docker
import requests
import time

# Initialize Docker client
client = docker.from_env()

# Hosts to simulate
HOSTS = ["host1", "host2"]

def create_networks():
    """Ensure networks exist"""
    for net_name in [EXTERNAL_NET, INTERNAL_NET]:
        try:
            client.networks.get(net_name)
            print(f"[+] Network {net_name} already exists")
        except docker.errors.NotFound:
            client.networks.create(net_name, driver="bridge")
            print(f"[+] Created network {net_name}")

def build_and_run(host, context_path):
    """Build image and run container attached to external"""
    print(f"[+] Building {host}")
    image, _ = client.images.build(path=context_path, tag=host)

    # Attach initially to external network
    print(f"[+] Running {host} on external network")
    container = client.containers.run(
        image,
        name=host,
        detach=True,
        tty=True,
        network=EXTERNAL_NET
    )
    return container

def check_compliance(hostname):
    """Call analyzer API to check compliance (dummy REST call)"""
    try:
        resp = requests.post("http://localhost:5000/check", json={"host": hostname})
        return resp.json().get("compliant", False)
    except Exception as e:
        print(f"[!] Analyzer check failed for {hostname}: {e}")
        return False

def move_to_internal(container):
    """Disconnect from external, attach to internal"""
    print(f"[+] Moving {container.name} to internal network")
    ext_net = client.networks.get(EXTERNAL_NET)
    int_net = client.networks.get(INTERNAL_NET)

    ext_net.disconnect(container)
    int_net.connect(container)

def run_scenario():
    """Full run for host1 + host2"""
    create_networks()

    # Start analyzer first
    analyzer = build_and_run("analyzer", "./Dockerfiles/analyzer")
    time.sleep(5)  # let analyzer boot

    results = {}
    for host in HOSTS:
        container = build_and_run(host, f"./Dockerfiles/scene1/{host}")
        time.sleep(3)

        compliant = check_compliance(host)
        results[host] = "Compliant" if compliant else "Non-compliant"

        if compliant:
            move_to_internal(container)

    print("[*] Scenario results:")
    for h, status in results.items():
        print(f"  {h}: {status}")

if __name__ == "__main__":
    run_scenario()
