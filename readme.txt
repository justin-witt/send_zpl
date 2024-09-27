ZPL PRINTER SENDER TOOL
=======================

This Python tool allows you to send ZPL (Zebra Programming Language) files to Zebra printers over the network. It supports both individual files and folders, providing options for either command-line use or interactive UI.

FEATURES
--------
- **Send ZPL files**: Send individual ZPL files or all valid files from a folder to a Zebra printer.
- **IP Address Validation**: Checks if the printer's IP is in a valid format before attempting a connection.
- **Printer Reachability**: Verifies if the printer is reachable before sending any data.
- **Command-Line and UI Support**: Use the command line for automation or enable the UI for interactive file selection.

PREREQUISITES
-------------
- Python 3.x
- The `ui_sender` module (included)
- Zebra printer supporting ZPL, network connected

INSTALLATION
------------
1. Clone the repository or download the script.

USAGE
-----

Command Line Options:

OPTION DESCRIPTION:
- `-target`: Printer's IP address.
- `-file`: Path to a single file to send to the printer.
- `-folder`: Path to a folder containing ZPL files to send.
- `-ui`: Enable the interactive UI mode for sending files.

INTERACTIVE MODE
----------------
If no command-line arguments are provided, the script will enter an interactive mode where it will prompt for the printer IP, file, or folder path.

TARGET FILE TYPES
-----------------
The script currently targets files with the `.105` extension for sending to the printer. You can customize this by modifying the `TARGET_FILE_TYPES` list in the script. You only need to update this in the "send_zpl.py" script if you are not running in ui mode.

NOTES
-----
- Ensure that your printer is reachable on the network and supports ZPL over port `9100`.
- If the provided IP is unreachable or the file path is invalid, appropriate error messages will be displayed.

------------------------------------------------------------------

For any issues or contributions, please create a pull request or open an issue on the repository.
