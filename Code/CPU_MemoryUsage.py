import psutil
import time
import csv
import os

def monitor_processes(duration=300, interval=5):
    process_data = {}
    start_time = time.time()
    
    while time.time() - start_time < duration:
        for proc in psutil.process_iter(attrs=['pid', 'name', 'exe']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                exe = proc.info['exe'] or "Unknown"
                cpu = proc.cpu_percent(interval=None) / psutil.cpu_count()
                mem = proc.memory_percent()
                
                if pid not in process_data:
                    process_data[pid] = {'name': name, 'exe': exe, 'cpu': [], 'mem': []}
                
                process_data[pid]['cpu'].append(cpu)
                process_data[pid]['mem'].append(mem)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        time.sleep(interval)
    
    return process_data

def calculate_averages(process_data):
    avg_data = []
    for pid, data in process_data.items():
        avg_cpu = sum(data['cpu']) / len(data['cpu']) if data['cpu'] else 0
        avg_mem = sum(data['mem']) / len(data['mem']) if data['mem'] else 0
        avg_data.append({'Process ID': pid, 'Process Name': data['name'], 'Average CPU (%)': avg_cpu, 'Average Memory (%)': avg_mem, 'Process File': data['exe']})
    
    return avg_data

def export_to_csv(data, output_path):
    if not data:
        return
    fieldnames = data[0].keys()
    with open(output_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    output_file = r"C:\\Temp\\CPU_Memory_Process_Average.csv"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    print("Monitoring processes for 5 minutes...")
    raw_data = monitor_processes()
    
    print("Calculating averages...")
    avg_data = calculate_averages(raw_data)
    
    print("Exporting data to CSV...")
    export_to_csv(avg_data, output_file)
    
    print(f"Data exported to {output_file}")

if __name__ == "__main__":
    main()
