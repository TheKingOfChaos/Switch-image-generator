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
    # Enterprise switch with custom VLAN assignments and port statuses
    
    # Define VLAN colors
    vlan_colors = {
        1: "#3498db",    # Default - Blue
        5: "#1abc9c",    # Internet Uplink - Turquoise
        10: "#2ecc71",   # Administration - Green
        20: "#e74c3c",   # Servere - Red
        30: "#f39c12",   # Netværksudstyr - Orange
        40: "#9b59b6",   # Kamera netværk - Purple
        50: "#16a085",   # Video Klienter - Dark Turquoise
        51: "#27ae60",   # GODIK - Dark Green
        60: "#e67e22",   # Almindelige klienter - Dark Orange
        70: "#d35400",   # Internet / Media - Darker Orange
        80: "#8e44ad",   # Guest Network - Dark Purple
        99: "#34495e",   # Trunk - Dark Blue/Gray
    }
    
    # Define VLAN assignments for each port
    port_vlan_map = {}
    
    # Ports 1-6: Trunk
    for port in range(1, 7):
        port_vlan_map[port] = 99
    
    # Ports 7-24: VLAN 40 (Kamera netværk)
    for port in range(7, 25):
        port_vlan_map[port] = 40
    
    # Ports 25-28: VLAN 50 (Video Klienter)
    for port in range(25, 29):
        port_vlan_map[port] = 50
    
    # Ports 29-32: VLAN 60 (Almindelige klienter)
    for port in range(29, 33):
        port_vlan_map[port] = 60
    
    # Ports 33-36: VLAN 70 (Internet / Media)
    for port in range(33, 37):
        port_vlan_map[port] = 70
    
    # Ports 37-40: VLAN 80 (Guest Network)
    for port in range(37, 41):
        port_vlan_map[port] = 80
    
    # Port 47: VLAN 30 (Netværksudstyr)
    port_vlan_map[47] = 30
    
    # Port 48: VLAN 10 (Administration)
    port_vlan_map[48] = 10
    
    # Define port statuses (ports 41-46 are disabled)
    port_status_map = {}
    for port in range(41, 47):
        port_status_map[port] = PortStatus.DISABLED
    
    # Define custom port labels (optional)
    port_labels = {

    }
    
    # Calculate the exact width needed for the ports
    # For 48 regular ports (24 columns) and 2 SFP ports (1 column):
    # 30 (start spacing) + 24 * (28 + 4) (regular ports) + 20 (sfp spacing) + 1 * 40 (sfp ports) + 20 (margins) = 874px
    exact_width = 30 + 24 * (28 + 4) + 20 + 40 + 20
    
    # Create the enterprise switch with SFP ports
    enterprise_switch = SwitchSVGGenerator(
        num_ports=48,
        switch_model=SwitchModel.ENTERPRISE,
        model_name="XS-4800-E",  # Custom model name
        switch_name="JMF-SW-001",
        port_vlan_map=port_vlan_map,
        port_status_map=port_status_map,
        port_labels=port_labels,
        vlan_colors=vlan_colors,
        sfp_ports=2,  # Add 2 SFP ports
        output_file="examples/output/enterprise_switch.svg",
        legend_items_spacing=10,  # Spacing between legend title and items
        legend_item_padding=3,  # Use negative padding to reduce space between items
        switch_width=exact_width  # Use the exact width needed for the ports
    )
    
    # Set SFP ports to Trunk VLAN (they will be ports 49 and 50)
    enterprise_switch.port_vlan_map[49] = 99
    enterprise_switch.port_vlan_map[50] = 99
    
    # Add labels for SFP ports
    enterprise_switch.port_labels[49] = "SFP1"
    enterprise_switch.port_labels[50] = "SFP2"
    
    enterprise_switch.save_svg()
    print("Created enterprise_switch.svg")
    
    print("\nEnterprise switch SVG has been generated. You can open it in a web browser to view.")

if __name__ == "__main__":
    main()
