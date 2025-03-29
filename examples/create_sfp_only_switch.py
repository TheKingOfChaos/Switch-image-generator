#!/usr/bin/env python3
"""
SFP-Only Switch Generator
------------------------
This script demonstrates how to create a switch with only SFP ports using the
SFP-only mode feature of the SwitchSVGGenerator.

In SFP-only mode:
- The switch has no regular RJ45 ports
- The number of SFP ports must be between 4 and 32
- Port numbering starts from 1
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus

def main():
    """Create switches with only SFP ports in different configurations."""
    
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Example 1: Basic SFP-only switch with 8 SFP ports in zigzag layout
    basic_sfp_switch = SwitchSVGGenerator(
        sfp_ports=8,
        sfp_only_mode=True,  # Enable SFP-only mode
        sfp_layout="zigzag",  # Use zigzag layout (default)
        switch_name="8-Port SFP Switch",
        switch_model=SwitchModel.ENTERPRISE,
        output_file="output/sfp_only_switch_zigzag.svg",
        theme=Theme.DARK,
        # Add some VLAN assignments for visual variety
        port_vlan_map={
            1: 10, 2: 10,  # First 2 ports on VLAN 10
            3: 20, 4: 20,  # Next 2 ports on VLAN 20
            5: 30, 6: 30,  # Next 2 ports on VLAN 30
            7: 40, 8: 40,  # Last 2 ports on VLAN 40
        },
        # Add some port statuses for visual variety
        port_status_map={
            2: PortStatus.DOWN,
            6: PortStatus.DISABLED,
        },
        # Add custom labels for SFP ports
        port_labels={
            1: "SFP1", 2: "SFP2", 3: "SFP3", 4: "SFP4",
            5: "SFP5", 6: "SFP6", 7: "SFP7", 8: "SFP8"
        }
    )
    basic_sfp_switch.save_svg()
    print("Generated SFP-only switch with zigzag layout: output/sfp_only_switch_zigzag.svg")
    
    # Example 2: SFP-only switch with 12 SFP ports in horizontal layout
    horizontal_sfp_switch = SwitchSVGGenerator(
        sfp_ports=12,
        sfp_only_mode=True,  # Enable SFP-only mode
        sfp_layout="horizontal",  # Use horizontal layout
        sfp_group_size=4,  # Group SFP ports in groups of 4
        switch_name="12-Port SFP Switch",
        switch_model=SwitchModel.DATA_CENTER,
        output_file="output/sfp_only_switch_horizontal.svg",
        theme=Theme.DARK,
        # Add some VLAN assignments for visual variety
        port_vlan_map={
            1: 10, 2: 10, 3: 10, 4: 10,  # First 4 ports on VLAN 10
            5: 20, 6: 20, 7: 20, 8: 20,  # Next 4 ports on VLAN 20
            9: 30, 10: 30, 11: 30, 12: 30,  # Last 4 ports on VLAN 30
        }
    )
    horizontal_sfp_switch.save_svg()
    print("Generated SFP-only switch with horizontal layout: output/sfp_only_switch_horizontal.svg")
    
    # Example 3: Maximum SFP-only switch with 32 SFP ports
    max_sfp_switch = SwitchSVGGenerator(
        sfp_ports=32,
        sfp_only_mode=True,  # Enable SFP-only mode
        sfp_layout="zigzag",  # Use zigzag layout
        sfp_group_size=8,  # Group SFP ports in groups of 8
        switch_width=1200,  # Wider switch to accommodate all ports
        switch_name="32-Port SFP Switch",
        switch_model=SwitchModel.DATA_CENTER,
        output_file="output/sfp_only_switch_max.svg",
        theme=Theme.DARK
    )
    max_sfp_switch.save_svg()
    print("Generated maximum SFP-only switch with 32 ports: output/sfp_only_switch_max.svg")
    
    print("\nAll SVG files have been generated in the 'output' directory.")
    print("You can open them in a web browser to view the different SFP-only switch configurations.")

if __name__ == "__main__":
    main()
