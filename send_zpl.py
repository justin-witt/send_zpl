import os
import re
import socket
import argparse
import ui_sender

# Define the constant list of target file types
TARGET_FILE_TYPES = ['.105']  # Add the file extensions you want to target

# Validate if the entered IP address is in a valid format
def validate_ip(ip_address):
    ip_pattern = re.compile(
        r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    )
    if ip_pattern.match(ip_address):
        return all(0 <= int(part) <= 255 for part in ip_address.split("."))
    return False

# Test if the printer at the IP address is reachable
def is_printer_reachable(ip_address, port=9100, timeout=2):
    try:
        with socket.create_connection((ip_address, port), timeout=timeout):
            return True
    except (socket.timeout, socket.error):
        return False

# Function to send the ZPL data to the printer
def send_zpl_to_printer(ip_address, file_path):
    with open(file_path, 'r') as file:
        zpl_data = file.read()
        
    try:
        with socket.create_connection((ip_address, 9100)) as sock:
            sock.sendall(zpl_data.encode())
    except socket.error as e:
        print(f"Error: Failed to send ZPL: {e}")

# Function to check if the file should be sent based on its extension
def should_send_file(file_name):
    return any(file_name.endswith(ext) for ext in TARGET_FILE_TYPES)

# Handle sending files from a folder
def send_folder(ip_address, folder_path):
    if not os.path.isdir(folder_path):
        print("Error: Provided folder path does not exist.")
        return
    
    for filename in os.listdir(folder_path):
        if should_send_file(filename):
            file_path = os.path.join(folder_path, filename)
            send_zpl_to_printer(ip_address, file_path)
    print(f"Success: ZPL sent to printer at {ip_address}")

# Handle command-line arguments and interactive user input
def main():
    parser = argparse.ArgumentParser(description="Send ZPL data to a printer.")
    parser.add_argument('-target', help="The IP address of the printer.")
    parser.add_argument('-file', help="Path to the file to send to the printer.")
    parser.add_argument('-folder', help="Path to the folder containing files to send to the printer.")
    parser.add_argument('-ui', action="store_true", help="Display the interactive user interface.")
    

    args = parser.parse_args()
    
    ip_address = args.target
    file_path = args.file
    folder_path = args.folder

    if args.ui:
        ui_sender.main(file_endings=TARGET_FILE_TYPES)
        return

    # If no arguments are provided, prompt for interactive input
    if not any([ip_address, file_path, folder_path]):
        ip_address = input("Enter the Printer's IP Address: ")

        if not validate_ip(ip_address):
            print("Error: Invalid IP Address format!")
            return

        if not is_printer_reachable(ip_address):
            print(f"Error: Cannot reach the printer at {ip_address}")
            return

        print("1. Send File")
        print("2. Send Folder")
        choice = input("Choose an option (1 or 2): ")

        if choice == '1':
            file_path = input("Enter the path to the file to send: ")
            if not os.path.isfile(file_path):
                print("Error: Provided file path does not exist.")
                return
            if not should_send_file(os.path.basename(file_path)):
                print("Error: File is not of a valid type.")
                return
            send_zpl_to_printer(ip_address, file_path)
            print(f"Success: ZPL sent to printer at {ip_address}")

        elif choice == '2':
            folder_path = input("Enter the path to the folder: ")
            send_folder(ip_address, folder_path)
        
        else:
            print("Error: Invalid choice.")
            return

    else:
        if not validate_ip(ip_address):
            print("Error: Invalid IP Address format!")
            return

        if not is_printer_reachable(ip_address):
            print(f"Error: Cannot reach the printer at {ip_address}")
            return

        if file_path and folder_path:
            print("Error: Cannot specify both file and folder.")
            return

        if file_path:
            if not os.path.isfile(file_path):
                print("Error: Provided file path does not exist.")
                return
            if not should_send_file(os.path.basename(file_path)):
                print("Error: File is not of a valid type.")
                return
            send_zpl_to_printer(ip_address, file_path)
            print(f"Success: ZPL sent to printer at {ip_address}")

        elif folder_path:
            send_folder(ip_address, folder_path)

        else:
            print("Error: Either file or folder must be specified.")

if __name__ == "__main__":
    main()
