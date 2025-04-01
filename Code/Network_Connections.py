import os
import csv
import psutil
import tkinter as tk

def get_network_connections(output_text, directory):
    filename = os.path.join(directory, "connections.csv")

    try:
        # Get all network connections
        connections = psutil.net_connections(kind='inet')  # 'inet' for IPv4/IPv6 connections

        # Open the CSV file for writing the connections
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Local Address", "Remote Address", "Status", "Process Name", "PID"])

            # Iterate through the connections and gather details
            for conn in connections:
                local_address = conn.laddr
                remote_address = conn.raddr if conn.raddr else None
                status = conn.status
                pid = conn.pid
                
                # Get process name using the PID
                try:
                    process_name = psutil.Process(pid).name() if pid else 'N/A'
                except psutil.NoSuchProcess:
                    process_name = 'N/A'

                # Write the connection info to the CSV file
                writer.writerow([local_address, remote_address, status, process_name, pid])

                # Print connection details to output_text widget
                output_text.insert(tk.END, f"Local Address: {local_address}, Remote Address: {remote_address}, "
                                          f"Status: {status}, Process: {process_name}, PID: {pid}\n")

        # Update the output text widget with the file save message
        output_text.insert(tk.END, f"\nNetwork connections information written to {filename}\n")
    except Exception as e:
        output_text.insert(tk.END, f"\nError: {str(e)}\n")
