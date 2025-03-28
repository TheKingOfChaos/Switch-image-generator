#!/usr/bin/env python3
"""
Example script to demonstrate how to create switches with consistent dimensions
regardless of theme or number of ports.

This ensures that both light and dark theme switches have the same dimensions
and that the legend is properly positioned in both cases.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, Theme, SwitchModel, PortStatus

def main():
    """Create example switches with consistent dimensions."""
    
    # Common parameters for consistent dimensions
    common_params = {
        "switch_width": 800,
        "switch_height": 130,  # Fixed height for all switches
        "legend_spacing": 30  # Increase spacing between switch and legend for better visibility
    }
    
    # Define VLAN assignments
    port_vlan_map = {
        1: 10,   # Port 1 on VLAN 10
        2: 10,   # Port 2 on VLAN 10
        3: 20,   # Port 3 on VLAN 20
        4: 20,   # Port 4 on VLAN 20
        5: 30,   # Port 5 on VLAN 30
        6: 30,   # Port 6 on VLAN 30
    }
    
    # Define port statuses
    port_status_map = {
        4: PortStatus.DOWN,      # Port 4 is down
        8: PortStatus.DISABLED,  # Port 8 is disabled
    }
    
    # Define custom port labels
    port_labels = {
        1: "WAN",
        2: "DMZ",
        3: "SRV1",
        4: "SRV2",
    }
    
    # Example 1: Light theme switch with legend outside
    light_switch = SwitchSVGGenerator(
        num_ports=48,
        output_file="../output/consistent_light_switch.svg",
        switch_model=SwitchModel.ENTERPRISE,
        switch_name="Light Theme Switch",
        theme=Theme.LIGHT,
        port_vlan_map=port_vlan_map,
        port_status_map=port_status_map,
        port_labels=port_labels,
        **common_params
    )
    light_switch.save_svg()
    print("Created ../output/consistent_light_switch.svg")
    
    # Example 2: Dark theme switch with legend outside
    
    dark_switch = SwitchSVGGenerator(
        num_ports=48,
        output_file="../output/consistent_dark_switch.svg",
        switch_model=SwitchModel.ENTERPRISE,
        switch_name="Dark Theme Switch",
        theme=Theme.DARK,
        port_vlan_map=port_vlan_map,
        port_status_map=port_status_map,
        port_labels=port_labels,
        **common_params
    )
    dark_switch.save_svg()
    print("Created ../output/consistent_dark_switch.svg")
    
    print("\nBoth switches have been generated with consistent dimensions.")
    print("The switch body height is fixed at 130px for both themes.")
    print("The legend is positioned outside the switch body in both cases.")

if __name__ == "__main__":
    main()
