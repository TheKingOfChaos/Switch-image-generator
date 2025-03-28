#!/usr/bin/env python3
"""
Create Single Row Switch
-----------------------
This script creates a network switch with one row of up to 24 normal ports
and 2 SFP ports as requested.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.single_row_switch_generator import SingleRowSwitchGenerator, SwitchModel, Theme

def main():
    """Create a switch with one row of up to 24 normal ports and 2 SFP ports."""
    
    # Create the switch with the requested configuration
    switch = SingleRowSwitchGenerator(
        num_ports=24,  # One row of up to 24 normal ports
        
        switch_model=SwitchModel.ENTERPRISE,  # Enterprise model for better appearance
        switch_width=1000,  # Wider to accommodate all ports in a single row
        switch_name="24-Port Switch with SFP (Single Row)",
        sfp_ports=2,  # Add 2 SFP ports as requested
        output_file="output/single_row_switch.svg",
        legend_spacing=30,  # Spacing between switch body and legend title
        legend_items_spacing=20,  # Spacing between legend title and legend items
        theme=Theme.DARK,  # Dark theme for better contrast
        # Optional: Add custom port labels for the SFP ports
        port_labels={
            25: "SFP1",
            26: "SFP2"
        }
    )
    
    # Generate and save the SVG
    switch.save_svg()
    print("Switch SVG generated as 'single_row_switch.svg'")
    
    # Optionally preview the SVG in a web browser
    switch.preview_svg()

if __name__ == "__main__":
    main()
