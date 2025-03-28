#!/usr/bin/env python3
"""
Test script to verify that the spacing is equal on both sides of the switch.
This script generates switches of different sizes and calculates the spacing on both sides.
"""

import os
from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme

def calculate_spacing(num_ports):
    """Calculate the spacing on both sides of the switch."""
    # Create a switch with the specified number of ports
    generator = SwitchSVGGenerator(
        num_ports=num_ports,
        switch_model=SwitchModel.ENTERPRISE,
        switch_name=f"{num_ports}-Port Switch",
        theme=Theme.DARK,
        output_file=f"output/{num_ports}_port_switch.svg"
    )
    
    # Calculate dimensions
    adjusted_width, adjusted_height, ports_per_row, num_rows = generator.calculate_dimensions()
    
    # Calculate the position of the first port
    start_spacing = 30  # Space from start of switch to first port
    left_spacing = start_spacing - 10  # 10px is the left margin of the switch body
    
    # Calculate the position of the last port
    regular_port_columns = (num_ports + 1) // 2  # Ceiling division for odd number of ports
    
    # For port grouping, we need to account for extra spacing
    port_grouping_extra_width = 0
    if generator.port_group_size > 0 and regular_port_columns > 0:
        # Calculate how many groups we have
        num_groups = (regular_port_columns + generator.port_group_size - 1) // generator.port_group_size
        # Calculate extra spacing from grouping
        port_grouping_extra_width = (num_groups - 1) * generator.port_group_spacing if num_groups > 1 else 0
    
    # Calculate the position of the last port
    last_port_x = start_spacing + (regular_port_columns - 1) * (generator.port_width + generator.port_spacing) + port_grouping_extra_width
    last_port_width = generator.port_width
    
    # Calculate the right spacing
    body_width = generator.body_width  # Use the body_width calculated in calculate_dimensions
    right_spacing = (10 + body_width) - (last_port_x + last_port_width)
    
    return left_spacing, right_spacing

def main():
    """Test the spacing for switches of different sizes."""
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Test switches with different numbers of ports
    port_counts = [8, 24, 48]
    
    print("Testing spacing for switches of different sizes:")
    print("------------------------------------------------")
    print(f"{'Ports':<10} {'Left Spacing':<15} {'Right Spacing':<15} {'Difference':<15}")
    print(f"{'-'*10:<10} {'-'*15:<15} {'-'*15:<15} {'-'*15:<15}")
    
    for num_ports in port_counts:
        left_spacing, right_spacing = calculate_spacing(num_ports)
        difference = abs(left_spacing - right_spacing)
        
        print(f"{num_ports:<10} {left_spacing:<15.2f} {right_spacing:<15.2f} {difference:<15.2f}")
    
    print("\nThe spacing should be equal (or very close) on both sides of the switch.")
    print("If the difference is more than 1-2 pixels, there may be an issue with the spacing calculation.")

if __name__ == "__main__":
    main()
