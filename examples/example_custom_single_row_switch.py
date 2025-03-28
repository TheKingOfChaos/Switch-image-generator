#!/usr/bin/env python3
"""
Example Custom Single Row Switch
-------------------------------
This script demonstrates how to create a customized single row switch
with different port configurations, VLAN assignments, and port statuses.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.single_row_switch_generator import SingleRowSwitchGenerator, SwitchModel, Theme, PortStatus

def main():
    """Create a customized single row switch with various configurations."""
    
    # Define VLAN assignments
    port_vlan_map = {
        1: 10,   # Port 1 on VLAN 10 (Management)
        2: 10,   # Port 2 on VLAN 10 (Management)
        3: 20,   # Port 3 on VLAN 20 (Users)
        4: 20,   # Port 4 on VLAN 20 (Users)
        5: 20,   # Port 5 on VLAN 20 (Users)
        6: 20,   # Port 6 on VLAN 20 (Users)
        7: 30,   # Port 7 on VLAN 30 (Servers)
        8: 30,   # Port 8 on VLAN 30 (Servers)
        9: 40,   # Port 9 on VLAN 40 (DMZ)
        10: 40,  # Port 10 on VLAN 40 (DMZ)
    }
    
    # Define port statuses
    port_status_map = {
        5: PortStatus.DOWN,      # Port 5 is down
        10: PortStatus.DISABLED, # Port 10 is disabled
    }
    
    # Define custom port labels
    port_labels = {
        1: "MGMT1",
        2: "MGMT2",
        7: "SRV1",
        8: "SRV2",
        9: "DMZ1",
        10: "DMZ2",
        # SFP port labels
        17: "UPLINK1",
        18: "UPLINK2",
    }
    
    # Define custom VLAN colors
    vlan_colors = {
        10: "#1E88E5",  # Blue for Management
        20: "#43A047",  # Green for Users
        30: "#E53935",  # Red for Servers
        40: "#FB8C00",  # Orange for DMZ
    }
    
    # Create the switch with the requested configuration
    switch = SingleRowSwitchGenerator(
        num_ports=16,  # 16 normal ports
        switch_width=900,  # Width to accommodate all ports
        switch_height=180,  # Standard height
        switch_model=SwitchModel.DATA_CENTER,  # Data center model
        switch_name="Custom Data Center Switch",
        sfp_ports=2,  # 2 SFP ports
        output_file="custom_single_row_switch.svg",
        legend_position="outside",  # Place legend outside
        theme=Theme.LIGHT,  # Light theme
        port_vlan_map=port_vlan_map,
        port_status_map=port_status_map,
        port_labels=port_labels,
        vlan_colors=vlan_colors
    )
    
    # Generate and save the SVG
    switch.save_svg()
    print("Custom switch SVG generated as 'custom_single_row_switch.svg'")
    
    # Optionally preview the SVG in a web browser
    switch.preview_svg()

if __name__ == "__main__":
    main()
