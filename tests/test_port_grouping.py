#!/usr/bin/env python3
"""
Test script to demonstrate the new port grouping feature.
This shows how to group ports in groups of X ports with additional spacing between groups.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, Theme, SwitchModel

# Create a switch with port grouping (4 ports per group)
switch_with_grouping = SwitchSVGGenerator(
    num_ports=24,
    switch_width=800,
    switch_height=130,
    output_file="switch_with_port_grouping.svg",
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Switch with Port Grouping (8 ports per group)",
    theme=Theme.LIGHT,
    sfp_ports=4,
    port_group_size=8,  # Group ports in groups of 4
    port_group_spacing=7  # Add 7px spacing between groups
)

# Generate and save the SVG
switch_with_grouping.save_svg()
print("Switch SVG with port grouping generated as 'switch_with_port_grouping.svg'")

# For comparison, create a switch without port grouping
switch_without_grouping = SwitchSVGGenerator(
    num_ports=24,
    switch_width=800,
    switch_height=130,
    output_file="switch_without_port_grouping.svg",
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Switch without Port Grouping",
    theme=Theme.LIGHT,
    sfp_ports=4
    # No port_group_size specified, so no grouping
)

# Generate and save the SVG
switch_without_grouping.save_svg()
print("Switch SVG without port grouping generated as 'switch_without_port_grouping.svg'")

print("\nCompare the two SVGs to see the difference in port spacing with grouping enabled.")
