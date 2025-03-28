#!/usr/bin/env python3
"""
Test script to verify that the canvas width follows the switch size
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.switch_svg_generator import SwitchSVGGenerator, PortStatus, SwitchModel, Theme, PortShape

def main():
    """Create test switches with different widths to verify canvas follows switch size."""
    
    # Test 1: Small switch (8 ports)
    small_switch = SwitchSVGGenerator(
        num_ports=8,
        switch_model=SwitchModel.BASIC,
        switch_name="Small Switch (8 ports)",
        output_file="output/small_width_test.svg",
    )
    small_switch.save_svg()
    print("Created small_width_test.svg")
    
    # Test 2: Medium switch (24 ports)
    medium_switch = SwitchSVGGenerator(
        num_ports=24,
        switch_model=SwitchModel.ENTERPRISE,
        switch_name="Medium Switch (24 ports)",
        output_file="output/medium_width_test.svg",
    )
    medium_switch.save_svg()
    print("Created medium_width_test.svg")
    
    # Test 3: Large switch (48 ports with SFP)
    # Define VLAN assignments for each port to create more legend items
    port_vlan_map = {}
    for i in range(1, 49):
        # Assign different VLANs to create more legend items
        port_vlan_map[i] = (i % 8) * 10  # VLANs 0, 10, 20, 30, 40, 50, 60, 70
    
    large_switch = SwitchSVGGenerator(
        num_ports=48,
        switch_model=SwitchModel.DATA_CENTER,
        switch_name="Large Switch (48 ports with SFP)",
        port_vlan_map=port_vlan_map,
        sfp_ports=2,
        output_file="output/large_width_test.svg",
    )
    large_switch.save_svg()
    print("Created large_width_test.svg")
    
    print("\nTest SVGs have been generated. You can open them in a web browser to view.")

if __name__ == "__main__":
    main()
