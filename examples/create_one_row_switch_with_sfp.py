#!/usr/bin/env python3
"""
One Row Switch Generator
-----------------------
This script generates an SVG image of a network switch with one row of up to 24 normal ports
and 2 SFP ports as requested.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme

def main():
    """Create a switch with one row of up to 24 normal ports and 2 SFP ports."""
    
    # Create the switch with the requested configuration
    switch = SwitchSVGGenerator(
        num_ports=24,  # One row of up to 24 normal ports
        switch_width=900,  # Wider to accommodate all ports in one row
        switch_height=200,  # Standard height
        switch_model=SwitchModel.ENTERPRISE,  # Enterprise model for better appearance
        switch_name="24-Port Switch with SFP",
        sfp_ports=2,  # Add 2 SFP ports as requested
        output_file="output/one_row_switch_with_sfp.svg",
        theme=Theme.DARK,  # Dark theme for better contrast
        # Optional: Add custom port labels for the SFP ports
        port_labels={
            25: "SFP1",
            26: "SFP2"
        }
    )
    
    # Generate and save the SVG
    switch.save_svg()
    print("Switch SVG generated as 'output/one_row_switch_with_sfp.svg'")
    
    # Optionally preview the SVG in a web browser
    switch.preview_svg()

if __name__ == "__main__":
    main()
