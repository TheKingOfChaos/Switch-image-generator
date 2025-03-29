#!/usr/bin/env python3
"""
Test Normal Switch Mode
----------------------
This script tests that the normal switch mode still works correctly after
adding the SFP-only mode feature. It creates a standard switch with regular
ports and SFP ports to verify that the original functionality is preserved.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus

def main():
    """Create a normal switch with regular ports and SFP ports."""
    
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Create a standard switch with 24 regular ports and 4 SFP ports
    normal_switch = SwitchSVGGenerator(
        num_ports=24,  # 24 regular ports
        sfp_ports=4,   # 4 SFP ports
        sfp_layout="zigzag",  # Use zigzag layout for SFP ports
        switch_name="24-Port Switch with 4 SFP Ports",
        switch_model=SwitchModel.ENTERPRISE,
        output_file="output/normal_switch_test.svg",
        theme=Theme.DARK,
        port_group_size=4,  # Group regular ports in groups of 4
        # Add some VLAN assignments for visual variety
        port_vlan_map={
            1: 10, 2: 10, 3: 10, 4: 10,  # First 4 ports on VLAN 10
            5: 20, 6: 20, 7: 20, 8: 20,  # Next 4 ports on VLAN 20
            9: 30, 10: 30, 11: 30, 12: 30,  # Next 4 ports on VLAN 30
            13: 40, 14: 40, 15: 40, 16: 40,  # Next 4 ports on VLAN 40
            17: 50, 18: 50, 19: 50, 20: 50,  # Next 4 ports on VLAN 50
            21: 60, 22: 60, 23: 60, 24: 60,  # Last 4 ports on VLAN 60
            25: 70, 26: 70,  # First 2 SFP ports on VLAN 70
            27: 80, 28: 80,  # Last 2 SFP ports on VLAN 80
        },
        # Add some port statuses for visual variety
        port_status_map={
            4: PortStatus.DOWN,
            8: PortStatus.DISABLED,
            26: PortStatus.DOWN,
            28: PortStatus.DISABLED,
        }
    )
    normal_switch.save_svg()
    print("Generated normal switch: output/normal_switch_test.svg")
    
    print("\nTest completed. The SVG file has been generated in the 'output' directory.")
    print("You can open it in a web browser to verify that the normal switch mode still works correctly.")

if __name__ == "__main__":
    main()
