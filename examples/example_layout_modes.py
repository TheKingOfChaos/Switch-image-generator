#!/usr/bin/env python3
"""
Example Layout Modes
-------------------
This script demonstrates the different layout modes available in the SwitchSVGGenerator.
It creates two switches: one with the default zigzag layout and one with the single row layout.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, LayoutMode

def main():
    """Create switches with different layout modes."""
    
    # Create a switch with the default zigzag layout
    zigzag_switch = SwitchSVGGenerator(
        num_ports=24,
        switch_model=SwitchModel.ENTERPRISE,
        switch_name="24-Port Switch (Zigzag Layout)",
        sfp_ports=2,
        output_file="examples/output/zigzag_layout_switch.svg",
        layout_mode=LayoutMode.ZIGZAG  # Default layout mode
    )
    
    # Generate and save the SVG
    zigzag_switch.save_svg()
    print("Zigzag layout switch SVG generated as 'examples/output/zigzag_layout_switch.svg'")
    
    # Create a switch with the single row layout
    single_row_switch = SwitchSVGGenerator(
        num_ports=24,
        switch_model=SwitchModel.ENTERPRISE,
        switch_name="24-Port Switch (Single Row Layout)",
        sfp_ports=2,
        output_file="examples/output/single_row_layout_switch.svg",
        layout_mode=LayoutMode.SINGLE_ROW  # Use single row layout
    )
    
    # Generate and save the SVG
    single_row_switch.save_svg()
    print("Single row layout switch SVG generated as 'examples/output/single_row_layout_switch.svg'")
    
    # Optionally preview the SVGs in a web browser
    # zigzag_switch.preview_svg()
    # single_row_switch.preview_svg()

if __name__ == "__main__":
    main()
