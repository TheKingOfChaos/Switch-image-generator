#!/usr/bin/env python3
"""
Example script demonstrating how to use the Network Switch SVG Generator GUI.
This script launches the GUI and shows how to programmatically set initial values.
"""

import os
import sys
import tkinter as tk

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import the GUI module
try:
    from gui import SwitchGeneratorGUI
except ImportError:
    print("Error: Could not import SwitchGeneratorGUI. Make sure the gui.py file is in the parent directory.")
    sys.exit(1)

def main():
    """Main function to run the GUI with custom initial values."""
    # Create the Tkinter root window
    root = tk.Tk()
    
    # Create the GUI application
    app = SwitchGeneratorGUI(root)
    
    # Set custom initial values (optional)
    app.layout_mode.set("single_row")  # Set layout mode to single row
    app.num_ports.set(24)              # Set number of ports to 24
    app.num_sfp_ports.set(2)           # Set number of SFP ports to 2
    app.theme.set("dark")              # Set theme to dark
    app.switch_model.set("enterprise") # Set switch model to enterprise
    app.switch_name.set("Core Switch") # Set switch name
    app.output_file.set("custom_switch.svg")  # Set output file
    
    # Update constraints based on the new values
    app.update_constraints()
    
    # Generate a preview with the new values
    app.generate_preview()
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
