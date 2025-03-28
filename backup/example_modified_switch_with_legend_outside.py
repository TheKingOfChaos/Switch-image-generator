#!/usr/bin/env python3
"""
Example script to generate a switch SVG with the requested modifications:
1. Fixed height for the switch
2. Legend placed under and outside the switch
3. Light gray background (the gray box is the switch)
4. Black legend text
"""

from switch_svg_generator import SwitchSVGGenerator, Theme, SwitchModel

# Create a switch with the requested modifications
switch = SwitchSVGGenerator(
    num_ports=24,
    switch_width=800,
    switch_height=130,  # Reduced height for the switch body
    output_file="modified_switch.svg",
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Modified Switch",
    theme=Theme.LIGHT,  # Light theme (light gray background and black text)
    sfp_ports=4,
    legend_position="outside"  # Place legend outside the switch
)

# Generate and save the SVG
switch.save_svg()
print("Modified switch SVG generated as 'modified_switch.svg'")
