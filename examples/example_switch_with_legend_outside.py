#!/usr/bin/env python3
"""
Example script to generate a switch SVG with the legend placed under and outside the switch.
This demonstrates the new legend_position="outside" parameter.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, Theme, SwitchModel

# Create a switch with the legend outside
switch = SwitchSVGGenerator(
    num_ports=24,
    switch_width=800,
    switch_height=130,  # Height of the switch body
    output_file="switch_with_legend_outside.svg",
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Switch with Legend Outside",
    theme=Theme.LIGHT,  # Light theme (light gray background and black text)
    sfp_ports=4
)

# Generate and save the SVG
switch.save_svg()
print("Switch SVG with legend outside generated as 'switch_with_legend_outside.svg'")
