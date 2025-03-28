#!/usr/bin/env python3
"""
Example usage of the SwitchSVGGenerator
---------------------------------------
This script demonstrates how to use the SwitchSVGGenerator class
to create custom network switch diagrams.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, PortStatus, SwitchModel, Theme, PortShape

def main():
    """Create example switch diagrams demonstrating various features."""
    
    # Example 1: Basic 24-port switch with default settings
    basic_switch = SwitchSVGGenerator(
        num_ports=24,
        output_file="../output/basic_switch.svg"
    )
    basic_switch.save_svg()
    print("Created basic_switch.svg")
    
    # Example 2: Enterprise switch with custom VLAN assignments and port statuses
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
    
    enterprise_switch = SwitchSVGGenerator(
        num_ports=48,
        switch_model=SwitchModel.ENTERPRISE,
        switch_name="Core Switch 1",
        port_vlan_map=port_vlan_map,
        port_status_map=port_status_map,
        port_labels=port_labels,
        output_file="../output/enterprise_switch.svg"
    )
    enterprise_switch.save_svg()
    print("Created enterprise_switch.svg")
    
    # Example 3: Data center switch with light theme and circular ports
    data_center_switch = SwitchSVGGenerator(
        num_ports=48,
        switch_model=SwitchModel.DATA_CENTER,
        switch_name="Data Center Switch",
        theme=Theme.LIGHT,
        port_shape=PortShape.CIRCULAR,
        output_file="../output/data_center_switch.svg"
    )
    data_center_switch.save_svg()
    print("Created data_center_switch.svg")
    
    # Example 4: Stackable switch with custom VLAN colors
    vlan_colors = {
        1: "#1E88E5",   # Custom blue for default VLAN
        10: "#43A047",  # Custom green for VLAN 10
        20: "#E53935",  # Custom red for VLAN 20
        30: "#FB8C00",  # Custom orange for VLAN 30
    }
    
    stackable_switch = SwitchSVGGenerator(
        num_ports=16,
        switch_model=SwitchModel.STACKABLE,
        switch_name="Access Switch",
        vlan_colors=vlan_colors,
        output_file="../output/stackable_switch.svg"
    )
    stackable_switch.save_svg()
    print("Created stackable_switch.svg")
    
    # Example 5: Switch with SFP ports
    # Define custom SFP port labels
    sfp_port_labels = {
    }
    
    sfp_switch = SwitchSVGGenerator(
        num_ports=48,
        switch_model=SwitchModel.ENTERPRISE,
        switch_name="Edge Switch with SFP",
        sfp_ports=6,  # Add 6 SFP ports to show the zigzag pattern
        port_labels=sfp_port_labels,
        output_file="../output/sfp_switch.svg"
    )
    sfp_switch.save_svg()
    print("Created sfp_switch.svg")
    
    print("\nAll example SVGs have been generated. You can open them in a web browser to view.")

if __name__ == "__main__":
    main()
