#!/usr/bin/env python3
"""
Script to fix the enterprise switch SVG to have consistent dimensions with the light theme switch.
This ensures the legend is properly positioned and visible.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.switch_svg_generator import SwitchSVGGenerator, PortStatus, SwitchModel, Theme

def main():
    """Create a fixed enterprise switch with consistent dimensions."""
    
    # Define VLAN assignments (same as in example_usage.py)
    port_vlan_map = {
        1: 10,   # Port 1 on VLAN 10
        2: 10,   # Port 2 on VLAN 10
        3: 20,   # Port 3 on VLAN 20
        4: 20,   # Port 4 on VLAN 20
        5: 30,   # Port 5 on VLAN 30
        6: 30,   # Port 6 on VLAN 30
    }
    
    # Define port statuses (same as in example_usage.py)
    port_status_map = {
        4: PortStatus.DOWN,      # Port 4 is down
        8: PortStatus.DISABLED,  # Port 8 is disabled
    }
    
    # Define custom port labels (same as in example_usage.py)
    port_labels = {
        1: "WAN",
        2: "DMZ",
        3: "SRV1",
        4: "SRV2",
    }
    
    # Create enterprise switch with fixed dimensions
    # Using the same height as the light theme example (130px)
    enterprise_switch = SwitchSVGGenerator(
        num_ports=48,
        switch_width=800,
        switch_height=130,  # Same height as light theme example
        switch_model=SwitchModel.ENTERPRISE,
        switch_name="Core Switch 1",
        port_vlan_map=port_vlan_map,
        port_status_map=port_status_map,
        port_labels=port_labels,
        theme=Theme.DARK,
        legend_position="outside",  # Explicitly set legend position
        output_file="fixed_enterprise_switch.svg"
    )
    
    # Generate and save the SVG
    enterprise_switch.save_svg()
    print("Created fixed_enterprise_switch.svg with consistent dimensions")

if __name__ == "__main__":
    main()
