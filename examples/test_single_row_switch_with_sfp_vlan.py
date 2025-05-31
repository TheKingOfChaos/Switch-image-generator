#!/usr/bin/env python3
"""
Test Single Row Switch with SFP VLAN Colors
-------------------------------------------
This script tests the SwitchSVGGenerator with single row layout and SFP ports using VLAN colors.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, PortStatus, LayoutMode

def main():
    """Create a single row switch with SFP ports using VLAN colors."""
    
    # Define port to VLAN mapping (including SFP ports)
    port_vlan_map = {
        1: 1,   # Default VLAN (blue)
        2: 10,  # VLAN 10 (green)
        3: 20,  # VLAN 20 (red)
        4: 30,  # VLAN 30 (orange)
        5: 40,  # VLAN 40 (purple)
        6: 50,  # VLAN 50 (turquoise)
        7: 1,   # Default VLAN (blue)
        8: 10,  # VLAN 10 (green)
        # SFP ports with different VLANs
        9: 20,  # SFP1 - VLAN 20 (red)
        10: 30  # SFP2 - VLAN 30 (orange)
    }
    
    # Define port status mapping
    port_status_map = {
        1: PortStatus.UP,       # Normal UP status
        2: PortStatus.UP,       # Normal UP status
        3: PortStatus.DOWN,     # DOWN status
        4: PortStatus.UP,       # Normal UP status
        5: PortStatus.DISABLED, # DISABLED status
        6: PortStatus.UP,       # Normal UP status
        7: PortStatus.DOWN,     # DOWN status
        8: PortStatus.UP,       # Normal UP status
        # SFP ports with different statuses
        9: PortStatus.UP,       # SFP1 - UP status
        10: PortStatus.DOWN     # SFP2 - DOWN status
    }
    
    # Create the single row switch
    switch = SwitchSVGGenerator(
        num_ports=8,            # 8 regular ports
        sfp_ports=2,            # 2 SFP ports
        port_vlan_map=port_vlan_map,
        port_status_map=port_status_map,
        switch_name="Single Row Switch with SFP VLAN Colors",
        output_file="output/single_row_switch_with_sfp_vlan.svg",
        show_status_indicator=True,
        layout_mode=LayoutMode.SINGLE_ROW  # Use single row layout
    )
    
    # Generate and save the SVG
    switch.save_svg()
    print("Switch SVG generated as 'output/single_row_switch_with_sfp_vlan.svg'")
    
    # Preview the SVG in a web browser
    switch.preview_svg()

if __name__ == "__main__":
    main()
