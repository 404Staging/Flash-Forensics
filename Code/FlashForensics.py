import tkinter as tk
from tkinter import ttk
import os
import zipfile
import shutil



import SystemInformation
import CPU_MemoryUsage
import Devices
import FileSystemStats
import Network_Connections
import usb_info
import userlogin
import Ping_Test

# GUI Setup
root = tk.Tk()
root.title("Flash Forensics")
root.configure(bg="#282828")

style = ttk.Style()
style.configure("TFrame", background="#282828")
style.configure("TLabel", foreground="white", background="#282828")
style.configure("TButton", foreground="black", background="#666666")

frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(frm, text="Flash Forensics", font=("Helvetica", 16, "bold")).grid(column=0, row=0, columnspan=2)

entry1 = ttk.Entry(frm, width=50)
entry1.insert(0, "C:\\temp\\")  
entry1.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

# Checkbox Variables
checkbox_vars = {
    "System Info": tk.IntVar(),
    "CPU/Memory Usage": tk.IntVar(),
    "Devices": tk.IntVar(),
    "File System": tk.IntVar(),
    "Network Connections": tk.IntVar(),
    "USB Info": tk.IntVar(),
    "User Logins": tk.IntVar(),
    "Ping Test": tk.IntVar()
}

# Checkboxes
for i, (label, var) in enumerate(checkbox_vars.items()):
    row, col = 3 + i // 2, i % 2
    tk.Checkbutton(frm, text=label, variable=var, bg="#282828", fg="white", selectcolor="#333333")\
        .grid(row=row, column=col, sticky="w", padx=30 if col == 0 else 10, pady=5)

# Message Output
message_text = tk.Text(frm, wrap=tk.WORD, width=50, height=15, bg="grey")
message_text.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

def start_selected_tasks():
    output_dir = entry1.get()
    os.makedirs(output_dir, exist_ok=True)
    csv_files = []

    def log(msg):
        message_text.insert(tk.END, msg + "\n")
        message_text.see(tk.END)

    try:
        if checkbox_vars["System Info"].get():
            path = os.path.join(output_dir, "SystemInformation.csv")
            SystemInformation.save_to_csv(path, [
                SystemInformation.get_device_name(),
                SystemInformation.get_windows_update_version(),
                *SystemInformation.get_network_info(),
                "; ".join(SystemInformation.get_physical_network_devices())
            ])
            csv_files.append(path)
            log("System Information collected.")

        if checkbox_vars["CPU/Memory Usage"].get():
            data = CPU_MemoryUsage.calculate_averages(
                CPU_MemoryUsage.monitor_processes(duration=10, interval=2)
            )
            path = os.path.join(output_dir, "CPU_Memory_Process_Average.csv")
            CPU_MemoryUsage.export_to_csv(data, path)
            csv_files.append(path)
            log("CPU/Memory Usage collected.")

        if checkbox_vars["Devices"].get():
            path = os.path.join(output_dir, "Devices.csv")
            Devices.save_to_csv(Devices.get_connected_devices(), path)
            csv_files.append(path)
            log("Devices collected.")

        if checkbox_vars["File System"].get():
            path = os.path.join(output_dir, "FileSystemStats.csv")
            drives = FileSystemStats.get_drive_usage()
            top_level = []
            for d in drives:
                drive_letter = d['Drive'].replace('\\', '')
                if os.path.exists(drive_letter):
                    top_level.extend(FileSystemStats.get_folder_sizes(drive_letter))
            users_folders = FileSystemStats.get_folder_sizes("C:\\Users")
            FileSystemStats.write_to_csv(path, drives, top_level, users_folders)
            csv_files.append(path)
            log("File system stats collected.")

        if checkbox_vars["Network Connections"].get():
            path = os.path.join(output_dir, "connections.csv")
            Network_Connections.get_network_connections(message_text, output_dir)
            csv_files.append(path)
            log("Network connections collected.")

        if checkbox_vars["USB Info"].get():
            path = os.path.join(output_dir, "usb.csv")
            usb_info.export_usb_info()
            if os.path.exists("usb.csv"):
                try:
                    shutil.move("usb.csv", path)
                except Exception:
                    shutil.copy2("usb.csv", path)
                    os.remove("usb.csv")
            csv_files.append(path)
            log("USB info collected.")

        if checkbox_vars["User Logins"].get():
            path = os.path.join(output_dir, "userslogins.csv")
            userlogin.export_to_csv(userlogin.get_windows_logins(), path)
            csv_files.append(path)
            log("User login info collected.")

        if checkbox_vars["Ping Test"].get():
            Ping_Test.main()
            path = os.path.join("C:\\Temp", "pingtest.csv")
            if os.path.exists(path):
                new_path = os.path.join(output_dir, "pingtest.csv")
                os.replace(path, new_path)
                csv_files.append(new_path)
                log("Ping test completed.")

        zip_path = os.path.join(output_dir, "FlashForensics_Report.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in csv_files:
                zipf.write(file, os.path.basename(file))
        log(f"Results zipped to {zip_path}")

        # Remove individual CSVs
        for file in csv_files:
            try:
                os.remove(file)
                log(f"Removed {file}")
            except Exception as e:
                log(f"Failed to remove {file}: {e}")

    except Exception as e:
        log(f"Error: {e}")

# Buttons
ttk.Button(frm, text="Run", command=start_selected_tasks).grid(column=0, row=7, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=10)
ttk.Button(frm, text="Stop", command=root.destroy).grid(column=0, row=8, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=10)

root.mainloop()
