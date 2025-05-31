#!/usr/bin/env python3
"""
Example script demonstrating how to create switches without using the GUI.
This script uses the SwitchSVGGenerator directly to create different switch configurations.
"""

import os
import sys

# Add the src directory to the Python path
src_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
sys.path.insert(0, src_dir)

# Import the switch generator
try:
    from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, LayoutMode
except ImportError:
    try:
        from switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, LayoutMode
    except ImportError:
        print("Error: Could not import SwitchSVGGenerator. Make sure the src directory is in your Python path.")
        sys.exit(1)

def create_enterprise_switch(output_file="enterprise_switch.svg"):
    """Create an enterprise switch and save it."""
    # Create the switch generator
    switch = SwitchSVGGenerator(
        num_ports=48,
        sfp_ports=6,
        layout_mode=LayoutMode.ZIGZAG,
        sfp_layout="zigzag",
        switch_model=SwitchModel.ENTERPRISE,
        switch_name="Enterprise Switch",
        theme=Theme.DARK,
        output_file=output_file
    )
    
    # Save the SVG
    switch.save_svg()
    
    print(f"Enterprise switch created and saved to {output_file}")

def create_data_center_switch(output_file="data_center_switch.svg"):
    """Create a data center switch and save it."""
    # Create the switch generator
    switch = SwitchSVGGenerator(
        num_ports=48,
        sfp_ports=6,
        layout_mode=LayoutMode.ZIGZAG,
        sfp_layout="horizontal",
        switch_model=SwitchModel.DATA_CENTER,
        switch_name="Data Center Switch",
        theme=Theme.LIGHT,
        output_file=output_file
    )
    
    # Save the SVG
    switch.save_svg()
    
    print(f"Data center switch created and saved to {output_file}")

def create_sfp_only_switch(output_file="sfp_only_switch.svg"):
    """Create an SFP-only switch and save it."""
    # Create the switch generator
    switch = SwitchSVGGenerator(
        sfp_ports=8,
        sfp_only_mode=True,
        sfp_layout="zigzag",
        switch_model=SwitchModel.STACKABLE,
        switch_name="SFP-Only Switch",
        theme=Theme.DARK,
        output_file=output_file
    )
    
    # Save the SVG
    switch.save_svg()
    
    print(f"SFP-only switch created and saved to {output_file}")

def main():
    """Main function to create different switch types."""
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Create an enterprise switch
    create_enterprise_switch(os.path.join(output_dir, "enterprise_switch.svg"))
    
    # Create a data center switch
    create_data_center_switch(os.path.join(output_dir, "data_center_switch.svg"))
    
    # Create an SFP-only switch
    create_sfp_only_switch(os.path.join(output_dir, "sfp_only_switch.svg"))
    
    print("\nAll switches created successfully!")
    print(f"Output files are in the {output_dir} directory.")

if __name__ == "__main__":
    main()
