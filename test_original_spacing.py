#!/usr/bin/env python3
"""
Test script to generate the original medium switch SVG for comparison.
"""

from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme

# Create a medium switch with enterprise model (24 ports)
generator = SwitchSVGGenerator(
    num_ports=24,
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Medium Switch (24 ports)",
    theme=Theme.DARK,
    output_file="output/medium_width_test.svg"
)

# Generate and save the SVG
generator.save_svg()

print("Generated original medium switch SVG at: output/medium_width_test.svg")
