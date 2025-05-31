#!/usr/bin/env python3
"""
Test script for the core functionality of the GUI without requiring a display.
This script tests the SwitchSVGGenerator integration with the GUI configuration.
"""

import os
import sys
import tempfile

# Add the src directory to the Python path
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_dir)

# Import the switch generator
try:
    from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus, LayoutMode
except ImportError:
    try:
        from switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus, LayoutMode
    except ImportError:
        print("Error: Could not import SwitchSVGGenerator. Make sure the src directory is in your Python path.")
        sys.exit(1)

def test_switch_generator():
    """Test the SwitchSVGGenerator with different configurations."""
    print("Testing SwitchSVGGenerator with different configurations...")
    
    # Create a temporary directory for the output files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test case 1: Single row layout
        print("\nTest case 1: Single row layout")
        output_file = os.path.join(temp_dir, "single_row_switch.svg")
        
        # Create port labels for SFP ports
        port_labels = {}
        num_ports = 24
        sfp_ports = 2
        for i in range(sfp_ports):
            port_labels[num_ports + i + 1] = f"SFP{i+1}"
        
        # Create the switch generator
        switch = SwitchSVGGenerator(
            num_ports=num_ports,
            switch_width=max(800, 30 + (num_ports * 32) + (sfp_ports * 44) + 30),
            switch_height=200,
            switch_model=SwitchModel.ENTERPRISE,
            switch_name="Single Row Switch",
            sfp_ports=sfp_ports,
            output_file=output_file,
            theme=Theme.DARK,
            port_labels=port_labels,
            layout_mode=LayoutMode.SINGLE_ROW
        )
        
        # Generate and save the SVG
        switch.save_svg()
        
        # Check if the file was created
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"  Success: Created {output_file} ({file_size} bytes)")
        else:
            print(f"  Error: Failed to create {output_file}")
        
        # Test case 2: Zigzag layout
        print("\nTest case 2: Zigzag layout")
        output_file = os.path.join(temp_dir, "zigzag_switch.svg")
        
        # Create port labels for SFP ports
        port_labels = {}
        num_ports = 48
        sfp_ports = 6
        for i in range(sfp_ports):
            port_labels[num_ports + i + 1] = f"SFP{i+1}"
        
        # Create the switch generator
        switch = SwitchSVGGenerator(
            num_ports=num_ports,
            switch_width=max(800, 30 + (num_ports * 16) + (sfp_ports * 44) + 30),
            switch_height=200,
            switch_model=SwitchModel.ENTERPRISE,
            switch_name="Zigzag Switch",
            sfp_ports=sfp_ports,
            output_file=output_file,
            theme=Theme.DARK,
            port_labels=port_labels,
            layout_mode=LayoutMode.ZIGZAG
        )
        
        # Generate and save the SVG
        switch.save_svg()
        
        # Check if the file was created
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"  Success: Created {output_file} ({file_size} bytes)")
        else:
            print(f"  Error: Failed to create {output_file}")
        
        # Test case 3: SFP-only mode
        print("\nTest case 3: SFP-only mode")
        output_file = os.path.join(temp_dir, "sfp_only_switch.svg")
        
        # Create port labels for SFP ports
        port_labels = {}
        sfp_ports = 8
        for i in range(sfp_ports):
            port_labels[i + 1] = f"SFP{i+1}"
        
        # Create the switch generator
        switch = SwitchSVGGenerator(
            sfp_ports=sfp_ports,
            sfp_only_mode=True,
            sfp_layout="zigzag",
            switch_width=max(800, 30 + (sfp_ports * 22) + 30),
            switch_height=200,
            switch_model=SwitchModel.ENTERPRISE,
            switch_name="SFP-Only Switch",
            output_file=output_file,
            theme=Theme.DARK,
            port_labels=port_labels
        )
        
        # Generate and save the SVG
        switch.save_svg()
        
        # Check if the file was created
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"  Success: Created {output_file} ({file_size} bytes)")
        else:
            print(f"  Error: Failed to create {output_file}")
    
    print("\nAll tests completed.")

if __name__ == "__main__":
    test_switch_generator()
