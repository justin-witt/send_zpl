import os
import re
import socket
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Define the constant list of target file types
TARGET_FILE_TYPES = ['.105', '.txt', '.zpl']  # Add the file extensions you want to target

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
        messagebox.showerror("Error", f"Failed to send ZPL: {e}")

# Function to check if the file should be sent based on its extension
def should_send_file(file_name):
    return any(file_name.endswith(ext) for ext in TARGET_FILE_TYPES)

# Prompt the user with buttons to send a file or all target file types in a folder
def select_files(ip_address):
    def send_file():
        file_path = filedialog.askopenfilename(title="Select a File")
        if file_path and should_send_file(os.path.basename(file_path)):
            send_zpl_to_printer(ip_address, file_path)
            messagebox.showinfo("Success", f"ZPL sent to printer at {ip_address}")
        else:
            messagebox.showwarning("Warning", "Selected file is not a valid type.")
        close_all_windows()
    
    def send_folder():
        folder_path = filedialog.askdirectory(title="Select a Folder")
        if folder_path:
            for filename in os.listdir(folder_path):
                if should_send_file(filename):
                    file_path = os.path.join(folder_path, filename)
                    send_zpl_to_printer(ip_address, file_path)
            messagebox.showinfo("Success", f"ZPL sent to printer at {ip_address}")
        close_all_windows()
    
    def close_all_windows():
        # Close the selection window and the root window
        selection_window.destroy()
        root.quit()

    # Create a new window for file/folder selection
    selection_window = tk.Toplevel()
    selection_window.title("Send ZPL")

    # Create buttons for file, folder, and exit
    file_button = tk.Button(selection_window, text="Send File", command=send_file)
    file_button.pack(pady=10)

    folder_button = tk.Button(selection_window, text="Send Folder", command=send_folder)
    folder_button.pack(pady=10)

    exit_button = tk.Button(selection_window, text="Exit", command=close_all_windows)
    exit_button.pack(pady=10)

    # Set the window size to 100x100 pixels
    selection_window.geometry("100x100")

    # Center the window on the screen
    selection_window.update_idletasks()  # Ensure the window has been drawn
    window_width = selection_window.winfo_width()
    window_height = selection_window.winfo_height()
    screen_width = selection_window.winfo_screenwidth()
    screen_height = selection_window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    selection_window.geometry(f"100x100+{x}+{y}")

    selection_window.mainloop()

# Main function
def main(file_endings : list = None):

    if file_endings:
        global TARGET_FILE_TYPES
        TARGET_FILE_TYPES = file_endings

    global root
    root = tk.Tk()
    
    # Hide the root window
    root.withdraw()

    # Get the IP address from the user
    ip_address = simpledialog.askstring("Send ZPL", "Enter the Printer's IP Address:")

    if not ip_address:
        root.quit()
        return

    if not validate_ip(ip_address):
        messagebox.showerror("Error", "Invalid IP Address format!")
        root.quit()
        return

    if not is_printer_reachable(ip_address):
        messagebox.showerror("Error", f"Cannot reach the printer at {ip_address}")
        root.quit()
        return

    # Prompt the user to choose between sending a file or folder
    select_files(ip_address)

if __name__ == "__main__":
    main()
