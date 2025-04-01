import os
import csv
import socket
import platform
import subprocess
import psutil

def get_device_name():
    return platform.node()

def get_windows_update_version():
    try:
        output = subprocess.check_output(
            "powershell.exe (Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion').DisplayVersion",
            shell=True, text=True
        )
        return output.strip()
    except Exception:
        return "Unknown"

def get_network_info():
    ip_address = "Unknown"
    subnet_mask = "Unknown"
    gateway = "Unknown"
    dns_servers = "Unknown"
    try:
        output = subprocess.check_output("ipconfig /all", shell=True, text=True)
        lines = output.split("\n")
        for i, line in enumerate(lines):
            if "IPv4 Address" in line:
                ip_address = line.split(":")[-1].strip().split("(")[0]
            elif "Subnet Mask" in line:
                subnet_mask = line.split(":")[-1].strip()
            elif "Default Gateway" in line:
                gateway = line.split(":")[-1].strip()
            elif "DNS Servers" in line:
                dns_servers = lines[i].split(":")[-1].strip()
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() and not lines[j].startswith(" "):
                        break
                    dns_servers += "; " + lines[j].strip()
    except Exception:
        pass
    return ip_address, subnet_mask, gateway, dns_servers

def get_physical_network_devices():
    devices = []
    try:
        output = subprocess.check_output("wmic nic where PhysicalAdapter=True get Name", shell=True, text=True)
        lines = output.split("\n")
        devices = [line.strip() for line in lines[1:] if line.strip()]
    except Exception:
        pass
    return devices

def save_to_csv(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Device Name", "Windows Update Version", "IP Address", "Subnet Mask", "Gateway", "DNS Servers", "Physical Network Devices"])
        writer.writerow(data)

def main():
    device_name = get_device_name()
    windows_update_version = get_windows_update_version()
    ip_address, subnet_mask, gateway, dns_servers = get_network_info()
    physical_devices = "; ".join(get_physical_network_devices())
    
    file_path = r"C:\\Temp\\SystemInformation.csv"
    save_to_csv(file_path, [device_name, windows_update_version, ip_address, subnet_mask, gateway, dns_servers, physical_devices])
    print(f"System information saved to {file_path}")

if __name__ == "__main__":
    main()
