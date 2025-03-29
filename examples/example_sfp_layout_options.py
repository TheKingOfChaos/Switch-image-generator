#!/usr/bin/env python3
"""
SFP Layout Options Example
-------------------------
This script demonstrates the different SFP port layout options available in the
SwitchSVGGenerator. It creates switches with the same configuration but
different SFP port layouts:
1. Horizontal layout - All SFP ports in a single horizontal row
2. Zigzag layout - SFP ports in a zigzag pattern (similar to regular ports)

It also demonstrates SFP port grouping with the horizontal layout.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus

def main():
    """Create switches with different SFP port layouts."""
    
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Common configuration for all switches
    common_config = {
        "num_ports": 24,  # 24 regular ports
        "sfp_ports": 6,   # 6 SFP ports
        "switch_width": 900,
        "switch_height": 150,
        "switch_model": SwitchModel.ENTERPRISE,
        "theme": Theme.DARK,
        "port_group_size": 4,  # Group regular ports in groups of 4
        "port_group_spacing": 10,  # 10px spacing between regular port groups
        # Add some VLAN assignments for visual variety
        "port_vlan_map": {
            1: 10, 2: 10, 3: 10, 4: 10,  # First 4 ports on VLAN 10
            5: 20, 6: 20, 7: 20, 8: 20,  # Next 4 ports on VLAN 20
            25: 30, 26: 30,  # First 2 SFP ports on VLAN 30
            27: 40, 28: 40,  # Next 2 SFP ports on VLAN 40
            29: 50, 30: 50,  # Last 2 SFP ports on VLAN 50
        },
        # Add some port statuses for visual variety
        "port_status_map": {
            4: PortStatus.DOWN,
            8: PortStatus.DISABLED,
            26: PortStatus.DOWN,
            28: PortStatus.DISABLED,
        },
        # Add custom labels for SFP ports
        "port_labels": {
            25: "SFP1", 26: "SFP2", 27: "SFP3",
            28: "SFP4", 29: "SFP5", 30: "SFP6"
        }
    }
    
    # 1. Create a switch with horizontal SFP layout (all SFP ports in a single row)
    horizontal_switch = SwitchSVGGenerator(
        **common_config,
        switch_name="Switch with Horizontal SFP Layout",
        output_file="output/sfp_horizontal_layout.svg",
        sfp_layout="horizontal",
        sfp_group_size=2  # Group SFP ports in pairs
    )
    horizontal_switch.save_svg()
    print("Generated switch with horizontal SFP layout: output/sfp_horizontal_layout.svg")
    
    # 2. Create a switch with zigzag SFP layout (similar to regular ports)
    zigzag_switch = SwitchSVGGenerator(
        **common_config,
        switch_name="Switch with Zigzag SFP Layout",
        output_file="output/sfp_zigzag_layout.svg",
        sfp_layout="zigzag",
        sfp_group_size=2  # Group SFP ports in pairs
    )
    zigzag_switch.save_svg()
    print("Generated switch with zigzag SFP layout: output/sfp_zigzag_layout.svg")
    
    # 4. Create a switch with horizontal SFP layout but no grouping
    horizontal_no_group_switch = SwitchSVGGenerator(
        **common_config,
        switch_name="Switch with Horizontal SFP Layout (No Grouping)",
        output_file="output/sfp_horizontal_no_grouping.svg",
        sfp_layout="horizontal",
        sfp_group_size=0  # No SFP port grouping
    )
    horizontal_no_group_switch.save_svg()
    print("Generated switch with horizontal SFP layout (no grouping): output/sfp_horizontal_no_grouping.svg")
    
    print("\nAll SVG files have been generated in the 'output' directory.")
    print("You can open them in a web browser to view the different SFP port layouts.")

if __name__ == "__main__":
    main()
