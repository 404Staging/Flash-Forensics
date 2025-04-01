import subprocess
import csv

def export_usb_info(output_file="usb.csv"):
    results = []
    try:
        # Run PowerShell to get USB device info
        ps_script = "Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -like '*USB*' } | Select-Object InstanceId, FriendlyName"
        process = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)

        lines = process.stdout.strip().splitlines()
        for line in lines[2:]:  # Skip header lines
            parts = line.strip().split(None, 1)
            if len(parts) == 2:
                results.append(parts)

        # Write results to CSV
        with open(output_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Device ID", "Friendly Name"])
            writer.writerows(results)

        print(f"USB device info exported to {output_file}")

    except Exception as e:
        print(f"Error collecting USB info: {e}")
