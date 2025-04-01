import os
import csv
import psutil

def get_drive_usage():
    """Returns a list of local drives and their usage statistics."""
    drives = []
    for partition in psutil.disk_partitions():
        if 'cdrom' in partition.opts or not os.path.exists(partition.mountpoint):
            continue
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            drives.append({
                'Drive': partition.device,
                'Total (GB)': round(usage.total / (1024**3), 2),
                'Used (GB)': round(usage.used / (1024**3), 2),
                'Free (GB)': round(usage.free / (1024**3), 2),
                'Usage (%)': usage.percent
            })
        except Exception as e:
            print(f"Error accessing drive {partition.device}: {e}")
    return drives

def get_folder_sizes(path):
    """Returns a list of top-level folders and their sizes within the given path."""
    folder_sizes = []
    if os.path.exists(path):
        for folder in os.listdir(path):
            folder_path = os.path.join(path, folder)
            if os.path.isdir(folder_path):
                total_size = 0
                try:
                    for dirpath, _, filenames in os.walk(folder_path):
                        for file in filenames:
                            file_path = os.path.join(dirpath, file)
                            try:
                                total_size += os.path.getsize(file_path)
                            except FileNotFoundError:
                                print(f"File not found: {file_path}")
                            except PermissionError:
                                print(f"Permission denied: {file_path}")
                except Exception as e:
                    print(f"Error accessing folder {folder_path}: {e}")
                folder_sizes.append({
                    'Folder': folder_path,
                    'Size (GB)': round(total_size / (1024**3), 2)
                })
    return folder_sizes

def write_to_csv(filepath, drives, top_level_folders, users_folders):
    """Writes the collected data to a CSV file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write drive usage
        writer.writerow(["Drive Usage Statistics"])
        writer.writerow(["Drive", "Total (GB)", "Used (GB)", "Free (GB)", "Usage (%)"])
        for drive in drives:
            writer.writerow(drive.values())
        writer.writerow([])
        
        # Write top-level folder sizes for each drive
        writer.writerow(["Top-Level Folder Sizes"])
        writer.writerow(["Folder", "Size (GB)"])
        for folder in top_level_folders:
            writer.writerow(folder.values())
        writer.writerow([])
        
        # Write C:\Users breakdown
        writer.writerow(["C:\\Users Folder Breakdown"])
        writer.writerow(["Folder", "Size (GB)"])
        for folder in users_folders:
            writer.writerow(folder.values())

def main():
    drives = get_drive_usage()
    top_level_folders = []
    
    # Get folder sizes for each drive
    for drive in drives:
        drive_letter = drive['Drive'].replace('\\', '')  # Remove trailing backslashes
        if os.path.exists(drive_letter):
            top_level_folders.extend(get_folder_sizes(drive_letter))
    
    # Get breakdown of C:\Users folder
    users_folders = get_folder_sizes("C:\\Users")
    
    # Write data to CSV
    write_to_csv("C:\\Temp\\FileSystemStats.csv", drives, top_level_folders, users_folders)
    print("Report saved to C:\\Temp\\FileSystemStats.csv")

if __name__ == "__main__":
    main()
