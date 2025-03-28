#!/usr/bin/env python3
"""
Example demonstrating custom model name
--------------------------------------
This script shows how to use the model_name parameter to display
a custom model name on the switch graphic.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme

def main():
    """Create example switches with custom model names."""
    
    # Example 1: Basic switch with custom model name
    basic_switch = SwitchSVGGenerator(
        num_ports=24,
        switch_model=SwitchModel.BASIC,  # Even with BASIC model, we can show a model name
        model_name="XS-2400-B",  # Custom model name
        switch_name="Basic Switch with Custom Model",
        output_file="output/custom_model_basic.svg"
    )
    basic_switch.save_svg()
    print("Created custom_model_basic.svg")
    
    # Example 2: Enterprise switch with custom model name
    enterprise_switch = SwitchSVGGenerator(
        num_ports=48,
        switch_model=SwitchModel.ENTERPRISE,
        model_name="XS-4800-E",  # Custom model name
        switch_name="Enterprise Switch with Custom Model",
        output_file="output/custom_model_enterprise.svg",
        sfp_ports=2
    )
    enterprise_switch.save_svg()
    print("Created custom_model_enterprise.svg")
    
    # Example 3: Data center switch with custom model name
    data_center_switch = SwitchSVGGenerator(
        num_ports=48,
        switch_model=SwitchModel.DATA_CENTER,
        model_name="XS-4800-DC",  # Custom model name
        switch_name="Data Center Switch with Custom Model",
        output_file="output/custom_model_data_center.svg",
        sfp_ports=4
    )
    data_center_switch.save_svg()
    print("Created custom_model_data_center.svg")
    
    print("\nCustom model name examples have been generated. You can open them in a web browser to view.")

if __name__ == "__main__":
    main()
