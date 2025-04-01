import subprocess
import csv
import os

def get_windows_logins():
    results = []
    try:
        output = subprocess.run(["query", "user"], capture_output=True, text=True)
        lines = output.stdout.strip().splitlines()[1:]  # Skip header
        for line in lines:
            parts = line.split()
            if len(parts) >= 6:
                username = parts[0]
                session_name = parts[1]
                logon_time = " ".join(parts[-2:])
                results.append({
                    "User": username,
                    "Session": session_name,
                    "Logon Time": logon_time
                })
    except Exception as e:
        print(f"Error reading login sessions: {e}")
    return results

def export_to_csv(events, output_path):
    if not events:
        return
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fieldnames = events[0].keys()
    with open(output_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(events)

if __name__ == "__main__":
    output_file = r"C:\\Temp\\userslogins.csv"
    export_to_csv(get_windows_logins(), output_file)
