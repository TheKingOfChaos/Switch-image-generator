#!/usr/bin/env python3
"""
Test Legend Spacing Values
-------------------------
This script demonstrates the effect of different legend_items_spacing values
on the generated SVG.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme

def main():
    """Create switches with different legend_items_spacing values."""
    
    # Test with different legend_items_spacing values
    spacing_values = [5, 10, 20, 30]
    
    for spacing in spacing_values:
        # Create a switch with the current spacing value
        switch = SwitchSVGGenerator(
            num_ports=24,
            switch_width=800,
            switch_model=SwitchModel.ENTERPRISE,
            switch_name=f"Legend Items Spacing: {spacing}px",
            sfp_ports=2,
            output_file=f"../output/legend_spacing_{spacing}px.svg",
            legend_items_spacing=spacing,  # Set the spacing value
            theme=Theme.DARK
        )
        
        # Generate and save the SVG
        switch.save_svg()
        print(f"Generated switch with legend_items_spacing={spacing}px")
    
    print("\nAll test SVGs have been generated. You can open them in a web browser to compare.")

if __name__ == "__main__":
    main()
