#!/usr/bin/env python3
"""
Example script demonstrating how to create a switch using the GUI and save it.
This script shows how to programmatically control the GUI to create a specific switch configuration.
"""

import os
import sys
import tkinter as tk
import time

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import the GUI module
try:
    from gui import SwitchGeneratorGUI
except ImportError:
    print("Error: Could not import SwitchGeneratorGUI. Make sure the gui.py file is in the parent directory.")
    sys.exit(1)

def create_enterprise_switch(output_file="enterprise_switch.svg"):
    """Create an enterprise switch using the GUI and save it."""
    # Create a root window that won't be shown
    root = tk.Tk()
    
    # Create the GUI application
    app = SwitchGeneratorGUI(root)
    
    # Configure the switch
    app.layout_mode.set("zigzag")       # Set layout mode to zigzag
    app.num_ports.set(48)               # Set number of ports to 48
    app.num_sfp_ports.set(6)            # Set number of SFP ports to 6
    app.sfp_layout.set("zigzag")        # Set SFP layout to zigzag
    app.theme.set("dark")               # Set theme to dark
    app.switch_model.set("enterprise")  # Set switch model to enterprise
    app.switch_name.set("Enterprise Switch")  # Set switch name
    app.output_file.set(output_file)    # Set output file
    
    # Update constraints based on the new values
    app.update_constraints()
    
    # Generate the switch
    app.save_svg()
    
    # Close the GUI
    root.destroy()
    
    print(f"Enterprise switch created and saved to {output_file}")

def create_data_center_switch(output_file="data_center_switch.svg"):
    """Create a data center switch using the GUI and save it."""
    # Create a root window that won't be shown
    root = tk.Tk()
    
    # Create the GUI application
    app = SwitchGeneratorGUI(root)
    
    # Configure the switch
    app.layout_mode.set("zigzag")        # Set layout mode to zigzag
    app.num_ports.set(48)                # Set number of ports to 48
    app.num_sfp_ports.set(6)             # Set number of SFP ports to 6
    app.sfp_layout.set("horizontal")     # Set SFP layout to horizontal
    app.theme.set("light")               # Set theme to light
    app.switch_model.set("data_center")  # Set switch model to data center
    app.switch_name.set("Data Center Switch")  # Set switch name
    app.output_file.set(output_file)     # Set output file
    
    # Update constraints based on the new values
    app.update_constraints()
    
    # Generate the switch
    app.save_svg()
    
    # Close the GUI
    root.destroy()
    
    print(f"Data center switch created and saved to {output_file}")

def create_sfp_only_switch(output_file="sfp_only_switch.svg"):
    """Create an SFP-only switch using the GUI and save it."""
    # Create a root window that won't be shown
    root = tk.Tk()
    
    # Create the GUI application
    app = SwitchGeneratorGUI(root)
    
    # Configure the switch
    app.sfp_only_mode.set(True)         # Set SFP-only mode
    app.num_sfp_ports.set(8)            # Set number of SFP ports to 8
    app.sfp_layout.set("zigzag")        # Set SFP layout to zigzag
    app.theme.set("dark")               # Set theme to dark
    app.switch_model.set("stackable")   # Set switch model to stackable
    app.switch_name.set("SFP-Only Switch")  # Set switch name
    app.output_file.set(output_file)    # Set output file
    
    # Update constraints based on the new values
    app.update_constraints()
    
    # Generate the switch
    app.save_svg()
    
    # Close the GUI
    root.destroy()
    
    print(f"SFP-only switch created and saved to {output_file}")

def main():
    """Main function to create different switch types."""
    # Create output directory if it doesn't exist
    output_dir = os.path.join(parent_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Create an enterprise switch
    create_enterprise_switch(os.path.join(output_dir, "enterprise_switch.svg"))
    
    # Create a data center switch
    create_data_center_switch(os.path.join(output_dir, "data_center_switch.svg"))
    
    # Create an SFP-only switch
    create_sfp_only_switch(os.path.join(output_dir, "sfp_only_switch.svg"))
    
    print("\nAll switches created successfully!")
    print(f"Output files are in the {output_dir} directory.")

if __name__ == "__main__":
    main()
