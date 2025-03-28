#!/usr/bin/env python3
"""
Test script to verify that the default legend position is now 'outside'
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator

def main():
    """Create a basic switch with default settings to test legend position"""
    
    # Create a basic switch with default settings
    # Since we've modified the default legend_position to "outside",
    # this should create a switch with the legend outside
    test_switch = SwitchSVGGenerator(
        num_ports=24,
        output_file="test_legend_outside.svg",
        switch_name="Test Switch - Default Legend Outside"
    )
    test_switch.save_svg()
    print("Created test_legend_outside.svg with default legend position")

if __name__ == "__main__":
    main()
