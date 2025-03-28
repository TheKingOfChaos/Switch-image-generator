#!/usr/bin/env python3
"""
Test for minimum width calculation
---------------------------------
This script tests that the switch width is correctly set to the minimum
width (10 normal ports + 1 SFP port) when a smaller switch is created.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme

def main():
    """Create a small switch to test minimum width calculation."""
    
    # Create a small switch with only 6 ports and 1 SFP port
    # This should use the minimum width (10 normal ports + 1 SFP port)
    small_switch = SwitchSVGGenerator(
        num_ports=6,
        switch_model=SwitchModel.BASIC,
        switch_name="Small Switch Test",
        sfp_ports=1,
        output_file="../output/minimum_width_test.svg",
        theme=Theme.DARK
    )
    
    small_switch.save_svg()
    print("Created minimum_width_test.svg")
    
    # Create another switch with exactly the minimum size (10 ports + 1 SFP)
    minimum_switch = SwitchSVGGenerator(
        num_ports=10,
        switch_model=SwitchModel.BASIC,
        switch_name="Minimum Size Switch",
        sfp_ports=1,
        output_file="../output/exact_minimum_size.svg",
        theme=Theme.DARK
    )
    
    minimum_switch.save_svg()
    print("Created exact_minimum_size.svg")
    
    # Create a larger switch (20 ports + 2 SFP)
    # This should be wider than the minimum
    larger_switch = SwitchSVGGenerator(
        num_ports=20,
        switch_model=SwitchModel.BASIC,
        switch_name="Larger Switch",
        sfp_ports=2,
        output_file="../output/larger_than_minimum.svg",
        theme=Theme.DARK
    )
    
    larger_switch.save_svg()
    print("Created larger_than_minimum.svg")
    
    print("\nAll test SVGs have been generated. You can open them in a web browser to view.")

if __name__ == "__main__":
    main()
