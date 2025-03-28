#!/usr/bin/env python3
"""
Test script to verify that the switch length is now dependent on the number of ports
while maintaining the minimum requirements:
1. No smaller than 8 normal ports and 2 SFP ports in one row
2. Same spacing from start of switch to first normal port
3. Same spacing from last SFP port to end of switch
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, Theme, SwitchModel

# Test 1: Small number of ports (less than minimum)
# This should create a switch with enough space for 8 normal ports and 2 SFP ports
small_switch = SwitchSVGGenerator(
    num_ports=5,  # Only 5 ports (minimum allowed), but should have space for at least 8
    switch_height=130,
    output_file="small_switch.svg",
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Small Switch (5 ports)",
    theme=Theme.LIGHT,
    sfp_ports=1  # Only 1 SFP port, but should have space for at least 2
)

# Generate and save the SVG
small_switch.save_svg()
print("Small switch SVG generated as 'small_switch.svg'")

# Test 2: Medium number of ports (exactly minimum)
medium_switch = SwitchSVGGenerator(
    num_ports=8,  # Exactly the minimum number of ports
    switch_height=130,
    output_file="medium_switch.svg",
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Medium Switch (8 ports)",
    theme=Theme.LIGHT,
    sfp_ports=2  # Exactly the minimum number of SFP ports
)

# Generate and save the SVG
medium_switch.save_svg()
print("Medium switch SVG generated as 'medium_switch.svg'")

# Test 3: Large number of ports (more than minimum)
large_switch = SwitchSVGGenerator(
    num_ports=24,  # More than the minimum number of ports
    switch_height=130,
    output_file="large_switch.svg",
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Large Switch (24 ports)",
    theme=Theme.LIGHT,
    sfp_ports=4  # More than the minimum number of SFP ports
)

# Generate and save the SVG
large_switch.save_svg()
print("Large switch SVG generated as 'large_switch.svg'")

# Test 4: Very large number of ports
very_large_switch = SwitchSVGGenerator(
    num_ports=48,  # Many ports
    switch_height=130,
    output_file="very_large_switch.svg",
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Very Large Switch (48 ports)",
    theme=Theme.LIGHT,
    sfp_ports=6  # Maximum number of SFP ports
)

# Generate and save the SVG
very_large_switch.save_svg()
print("Very large switch SVG generated as 'very_large_switch.svg'")

print("\nAll test SVGs generated. The switch length should now be dependent on the number of ports,")
print("but no smaller than what would fit 8 normal ports and 2 SFP ports in one row.")
print("The spacing from the start of the switch to the first port and from the last SFP port")
print("to the end of the switch should be consistent across all switch sizes.")
