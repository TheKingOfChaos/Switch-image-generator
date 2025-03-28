#!/usr/bin/env python3
"""
Example script to generate a switch SVG with the requested modifications:
1. Fixed height for the switch
2. Legend placed inside the switch (not outside)
3. Light gray background (the gray box is the switch)
4. Black legend text
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, Theme, SwitchModel

# Create a switch with the requested modifications
switch = SwitchSVGGenerator(
    num_ports=24,
    switch_width=800,
    switch_height=150,  # Fixed height for the switch
    output_file="modified_switch.svg",
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Modified Switch",
    theme=Theme.LIGHT,  # Light theme (light gray background and black text)
    sfp_ports=4,
    legend_position="inside"  # Default: place legend inside the switch
)

# Generate and save the SVG
switch.save_svg()
print("Modified switch SVG generated as 'modified_switch.svg'")
