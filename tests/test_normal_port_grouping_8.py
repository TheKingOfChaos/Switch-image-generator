#!/usr/bin/env python3
"""
Test script to demonstrate port grouping with normal ports.
This shows how to group ports in groups of X ports with additional spacing between groups.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, Theme, SwitchModel, PortStatus

def main():
    """Create example switches with different port grouping configurations"""
    
    # Define VLAN colors
    vlan_colors = {
        1: "#3498db",    # Default - Blue
        10: "#2ecc71",   # Green
        20: "#e74c3c",   # Red
        30: "#f39c12",   # Orange
        40: "#9b59b6",   # Purple
        50: "#1abc9c",   # Turquoise
    }
    
    # Define port to VLAN mapping for better visualization of port groups
    port_vlan_map = {}
    
    # Alternate VLANs for each port group to make grouping more visible
    # For groups of 8: VLAN 10, 20, 30, 10, 20, ...
    for i in range(1, 25):
        group_num = (i - 1) // 8
        vlan_id = [10, 20, 30][group_num % 3]
        port_vlan_map[i] = vlan_id
    
    # Create a switch with port grouping (4 ports per group)
    switch_with_grouping = SwitchSVGGenerator(
        num_ports=24,
        switch_width=800,
        switch_height=130,
        output_file="normal_port_grouping_8.svg",
        switch_model=SwitchModel.ENTERPRISE,
        switch_name="Switch with Port Grouping (8 ports per group)",
        theme=Theme.LIGHT,
        vlan_colors=vlan_colors,
        port_vlan_map=port_vlan_map,
        sfp_ports=2,  # Add 2 SFP ports
        port_group_size=8,  # Group ports in groups of 8
        port_group_spacing=10 # Add 7px spacing between groups
    )
    
    # Set SFP ports to VLAN 50 (they will be ports 25 and 26)
    switch_with_grouping.port_vlan_map[25] = 50
    switch_with_grouping.port_vlan_map[26] = 50
    
    # Generate and save the SVG
    switch_with_grouping.save_svg()
    print("Switch SVG with port grouping (8 ports per group) generated as 'normal_port_grouping_8.svg'")
    
   
if __name__ == "__main__":
    main()
