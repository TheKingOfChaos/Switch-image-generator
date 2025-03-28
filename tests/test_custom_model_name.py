#!/usr/bin/env python3
"""
Test script to verify that custom model names are displayed correctly.
This tests the model_name parameter that allows specifying a custom model name.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, Theme, SwitchModel

def main():
    """Create test switches with custom model names."""
    
    # Test 1: Enterprise switch with custom model name
    enterprise_switch = SwitchSVGGenerator(
        num_ports=24,
        switch_width=800,
        switch_height=130,
        output_file="tests/output/custom_model_enterprise.svg",
        switch_model=SwitchModel.ENTERPRISE,
        model_name="XS-2400-E",  # Custom model name
        switch_name="Enterprise Switch with Custom Model",
        theme=Theme.DARK,
        sfp_ports=2
    )
    
    # Generate and save the SVG
    enterprise_switch.save_svg()
    print("Enterprise switch with custom model name generated as 'tests/output/custom_model_enterprise.svg'")
    
    # Test 2: Basic switch with custom model name
    # This tests that even with BASIC model (which normally doesn't show model info),
    # a custom model name will be displayed
    basic_switch = SwitchSVGGenerator(
        num_ports=24,
        switch_width=800,
        switch_height=130,
        output_file="tests/output/custom_model_basic.svg",
        switch_model=SwitchModel.BASIC,
        model_name="XS-2400-B",  # Custom model name
        switch_name="Basic Switch with Custom Model",
        theme=Theme.DARK,
        sfp_ports=0  # Test with 0 SFP ports to verify our fix
    )
    
    # Generate and save the SVG
    basic_switch.save_svg()
    print("Basic switch with custom model name generated as 'tests/output/custom_model_basic.svg'")
    
    # Test 3: Default behavior - no custom model name provided
    # This tests that when no custom model name is provided, it falls back to the enum value
    default_switch = SwitchSVGGenerator(
        num_ports=24,
        switch_width=800,
        switch_height=130,
        output_file="tests/output/default_model_name.svg",
        switch_model=SwitchModel.DATA_CENTER,
        # No model_name provided, should use "data_center"
        switch_name="Switch with Default Model Name",
        theme=Theme.DARK,
        sfp_ports=2
    )
    
    # Generate and save the SVG
    default_switch.save_svg()
    print("Switch with default model name generated as 'tests/output/default_model_name.svg'")
    
    print("\nTest completed. Check the SVG files to verify that model names are displayed correctly.")
    print("For the basic switch, verify that the model name is displayed even though it's a basic model.")
    print("For the default switch, verify that it falls back to the enum value ('data_center').")

if __name__ == "__main__":
    main()
