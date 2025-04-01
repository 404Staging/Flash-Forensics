import csv
import subprocess
import socket
import os

def ping(host):
    """Pings a host and returns True if successful, False otherwise."""
    try:
        output = subprocess.run(["ping", "-n", "2", host], capture_output=True, text=True)
        return "Reply from" in output.stdout
    except Exception as e:
        return False

def get_default_gateway():
    """Retrieves the default gateway IP address."""
    try:
        output = subprocess.run("ipconfig", capture_output=True, text=True)
        for line in output.stdout.split("\n"):
            if "Default Gateway" in line:
                return line.split()[-1]
    except Exception:
        pass
    return "Unknown"

def get_local_ip():
    """Gets the local machine's IP address."""
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return "Unknown"

def main():
    results = []
    
    # Loopback test
    results.append(["Loopback (127.0.0.1)", "127.0.0.1", ping("127.0.0.1")])
    
    # Local IP test
    local_ip = get_local_ip()
    results.append(["Local IP", local_ip, ping(local_ip)])
    
    # Default Gateway test
    default_gateway = get_default_gateway()
    results.append(["Default Gateway", default_gateway, ping(default_gateway)])
    
    # Google test
    results.append(["Google", "google.com", ping("google.com")])
    
    # Ensure the directory exists
    os.makedirs("C:\\Temp", exist_ok=True)
    output_file = "C:\\Temp\\pingtest.csv"
    
    # Write to CSV
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Target", "IP Address", "Reachable"])
        writer.writerows(results)
    
    print(f"Ping test results saved to {output_file}")

if __name__ == "__main__":
    main()
