#!/usr/bin/env python3
"""
Test Legend Spacing
------------------
This script demonstrates the independent control of spacing between:
1. The switch body and the legend title
2. The legend title and the legend items
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.single_row_switch_generator import SingleRowSwitchGenerator, SwitchModel, Theme

def main():
    """Create a switch with custom legend spacing values."""
    
    # Create the switch with custom legend spacing
    switch = SingleRowSwitchGenerator(
        num_ports=24,
        switch_width=1000,
        switch_model=SwitchModel.ENTERPRISE,
        switch_name="Switch with Custom Legend Spacing",
        sfp_ports=2,
        output_file="output/custom_legend_spacing.svg",
        # Custom spacing values
        legend_spacing=40,  # Increased spacing between switch body and legend title
        legend_items_spacing=30,  # Increased spacing between legend title and items
        theme=Theme.DARK,
        port_labels={
            25: "SFP1",
            26: "SFP2"
        }
    )
    
    # Generate and save the SVG
    switch.save_svg()
    print("Switch SVG generated as 'custom_legend_spacing.svg'")
    
    # Optionally preview the SVG in a web browser
    switch.preview_svg()

if __name__ == "__main__":
    main()
