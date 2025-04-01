import subprocess
import csv
import os

def get_connected_devices():
    devices = []
    result = subprocess.run(
        ["wmic", "path", "Win32_PnPEntity", "get", "DeviceID,Description,Manufacturer,Name,Status", "/format:csv"],
        capture_output=True,
        text=True
    )

    lines = result.stdout.strip().splitlines()
    if not lines:
        return devices

    headers = [h.strip() for h in lines[0].split(",")]
    for line in lines[1:]:
        if line.strip() == "" or line.startswith("Node"):
            continue
        fields = [f.strip() for f in line.split(",")]
        if len(fields) == len(headers):
            devices.append(fields)

    return devices

def save_to_csv(devices, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Node", "DeviceID", "Description", "Manufacturer", "Name", "Status"])
        writer.writerows(devices)

if __name__ == "__main__":
    output = get_connected_devices()
    save_to_csv(output, "C:\\Temp\\Devices.csv")
