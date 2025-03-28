#!/usr/bin/env python3
"""
Example script to generate a switch SVG with custom colors for the switch body and border.
This demonstrates the new switch_body_color and switch_body_border_color parameters.
"""

from switch_svg_generator import SwitchSVGGenerator, Theme, SwitchModel

# Create a switch with custom colors
switch = SwitchSVGGenerator(
    num_ports=24,
    switch_width=800,
    switch_height=130,  # Height of the switch body
    output_file="custom_switch_colors.svg",
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Custom Colored Switch",
    theme=Theme.LIGHT,  # Light theme for the background
    sfp_ports=4,
    legend_position="outside",  # Place legend outside and below the switch
    switch_body_color="#4a86e8",  # Custom blue color for the switch body
    switch_body_border_color="#000000",  # Black border
    switch_body_border_width=2  # 2px border width
)

# Generate and save the SVG
switch.save_svg()
print("Switch SVG with custom colors generated as 'custom_switch_colors.svg'")
