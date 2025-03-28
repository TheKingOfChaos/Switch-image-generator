#!/usr/bin/env python3
"""
Test script to verify that the permanent fix in switch_svg_generator.py works correctly.
This script generates a medium switch SVG directly with the modified SwitchSVGGenerator class.
"""

from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme

# Create a medium switch with enterprise model (24 ports)
generator = SwitchSVGGenerator(
    num_ports=24,
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Medium Switch (24 ports)",
    theme=Theme.DARK,
    output_file="output/medium_width_permanent_fix.svg"
)

# Generate and save the SVG
generator.save_svg()

print("Generated medium switch SVG with permanent fix at: output/medium_width_permanent_fix.svg")
