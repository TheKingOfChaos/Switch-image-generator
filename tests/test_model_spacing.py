#!/usr/bin/env python3
"""
Test script to verify that model spacing is consistent even when using the basic model.
This demonstrates the fix for "add model spacing even i empty".
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, Theme, SwitchModel

# Create a switch with basic model (previously had inconsistent spacing)
basic_switch = SwitchSVGGenerator(
    num_ports=24,
    switch_width=800,
    switch_height=130,
    output_file="basic_model_switch.svg",
    switch_model=SwitchModel.BASIC,  # Using basic model
    switch_name="Basic Model Switch",
    theme=Theme.LIGHT,
    sfp_ports=4
)

# Generate and save the SVG
basic_switch.save_svg()
print("Basic model switch SVG generated as 'basic_model_switch.svg'")

# For comparison, create a switch with enterprise model (already had correct spacing)
enterprise_switch = SwitchSVGGenerator(
    num_ports=24,
    switch_width=800,
    switch_height=130,
    output_file="enterprise_model_switch.svg",
    switch_model=SwitchModel.ENTERPRISE,  # Using enterprise model
    switch_name="Enterprise Model Switch",
    theme=Theme.LIGHT,
    sfp_ports=4
)

# Generate and save the SVG
enterprise_switch.save_svg()
print("Enterprise model switch SVG generated as 'enterprise_model_switch.svg'")
