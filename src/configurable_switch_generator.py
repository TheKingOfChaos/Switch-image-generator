#!/usr/bin/env python3
"""
Configurable Switch Generator
----------------------------
This script allows you to generate a network switch SVG with configurable layout:
1. One row with up to 24 normal ports and 2 SFP ports
2. Two rows with up to 48 normal ports and 6 SFP ports

Usage:
  python3 configurable_switch_generator.py --layout single --ports 24 --sfp 2
  python3 configurable_switch_generator.py --layout double --ports 48 --sfp 6
  python3 configurable_switch_generator.py --interactive
"""

import argparse
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus
from single_row_switch_generator import SingleRowSwitchGenerator

def generate_switch(layout_type, num_ports, sfp_ports, output_file, switch_name=None, theme=Theme.DARK):
    """
    Generate a switch SVG based on the specified layout type and configuration.
    
    Args:
        layout_type: 'single' for single row, 'double' for double row (zigzag)
        num_ports: Number of normal ports
        sfp_ports: Number of SFP ports
        output_file: Output SVG filename
        switch_name: Custom name for the switch (optional)
        theme: Color theme (optional)
    """
    # Validate inputs
    if layout_type == 'single':
        if num_ports > 24:
            print(f"Warning: Single row layout supports max 24 ports. Limiting to 24.")
            num_ports = 24
        if sfp_ports > 2:
            print(f"Warning: Single row layout supports max 2 SFP ports. Limiting to 2.")
            sfp_ports = 2
        
        # Set default switch name if not provided
        if not switch_name:
            switch_name = f"{num_ports}-Port Switch with {sfp_ports} SFP (Single Row)"
        
        # Create SFP port labels
        port_labels = {}
        for i in range(sfp_ports):
            port_labels[num_ports + i + 1] = f"SFP{i+1}"
        
        # Create single row switch
        switch = SingleRowSwitchGenerator(
            num_ports=num_ports,
            switch_width=max(800, 30 + (num_ports * 32) + (sfp_ports * 44) + 30),  # Dynamic width based on ports
            switch_height=180,
            switch_model=SwitchModel.ENTERPRISE,
            switch_name=switch_name,
            sfp_ports=sfp_ports,
            output_file=output_file,
            legend_position="outside",
            theme=theme,
            port_labels=port_labels
        )
    else:  # double row (zigzag)
        if num_ports > 48:
            print(f"Warning: Double row layout supports max 48 ports. Limiting to 48.")
            num_ports = 48
        if sfp_ports > 6:
            print(f"Warning: Double row layout supports max 6 SFP ports. Limiting to 6.")
            sfp_ports = 6
        
        # Set default switch name if not provided
        if not switch_name:
            switch_name = f"{num_ports}-Port Switch with {sfp_ports} SFP (Double Row)"
        
        # Create SFP port labels
        port_labels = {}
        for i in range(sfp_ports):
            port_labels[num_ports + i + 1] = f"SFP{i+1}"
        
        # Create double row (zigzag) switch
        switch = SwitchSVGGenerator(
            num_ports=num_ports,
            switch_width=max(800, 30 + (num_ports * 16) + (sfp_ports * 44) + 30),  # Dynamic width based on ports
            switch_height=200,
            switch_model=SwitchModel.ENTERPRISE,
            switch_name=switch_name,
            sfp_ports=sfp_ports,
            output_file=output_file,
            legend_position="outside",
            theme=theme,
            port_labels=port_labels
        )
    
    # Generate and save the SVG
    switch.save_svg()
    print(f"Switch SVG generated as '{output_file}'")
    
    # Preview the SVG in a web browser
    switch.preview_svg()

def interactive_mode():
    """Run the generator in interactive mode, prompting the user for input."""
    print("Configurable Switch Generator - Interactive Mode")
    print("-----------------------------------------------")
    
    # Prompt for layout type
    while True:
        layout_choice = input("Select layout type (1=Single Row, 2=Double Row): ").strip()
        if layout_choice in ['1', '2']:
            break
        print("Invalid choice. Please enter 1 or 2.")
    
    layout_type = 'single' if layout_choice == '1' else 'double'
    
    # Prompt for number of ports
    max_ports = 24 if layout_type == 'single' else 48
    while True:
        try:
            num_ports = int(input(f"Number of normal ports (1-{max_ports}): ").strip())
            if 1 <= num_ports <= max_ports:
                break
            print(f"Invalid number. Please enter a value between 1 and {max_ports}.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Prompt for number of SFP ports
    max_sfp = 2 if layout_type == 'single' else 6
    while True:
        try:
            sfp_ports = int(input(f"Number of SFP ports (0-{max_sfp}): ").strip())
            if 0 <= sfp_ports <= max_sfp:
                break
            print(f"Invalid number. Please enter a value between 0 and {max_sfp}.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Prompt for output filename
    default_filename = f"{'single' if layout_type == 'single' else 'double'}_row_switch_{num_ports}p_{sfp_ports}sfp.svg"
    output_file = input(f"Output filename [{default_filename}]: ").strip()
    if not output_file:
        output_file = default_filename
    
    # Prompt for theme
    while True:
        theme_choice = input("Select theme (1=Dark, 2=Light) [1]: ").strip()
        if not theme_choice:
            theme_choice = '1'
        if theme_choice in ['1', '2']:
            break
        print("Invalid choice. Please enter 1 or 2.")
    
    theme = Theme.DARK if theme_choice == '1' else Theme.LIGHT
    
    # Generate the switch
    generate_switch(layout_type, num_ports, sfp_ports, output_file, theme=theme)

def main():
    """Parse command-line arguments and generate the switch."""
    parser = argparse.ArgumentParser(description='Generate a network switch SVG with configurable layout.')
    
    # Add arguments
    parser.add_argument('--layout', choices=['single', 'double'], 
                        help='Layout type: single for one row, double for two rows (zigzag)')
    parser.add_argument('--ports', type=int, help='Number of normal ports')
    parser.add_argument('--sfp', type=int, help='Number of SFP ports')
    parser.add_argument('--output', help='Output SVG filename')
    parser.add_argument('--name', help='Custom switch name')
    parser.add_argument('--theme', choices=['dark', 'light'], default='dark', 
                        help='Color theme (default: dark)')
    parser.add_argument('--interactive', action='store_true', 
                        help='Run in interactive mode (prompts for input)')
    
    args = parser.parse_args()
    
    # Check if interactive mode is requested
    if args.interactive:
        interactive_mode()
        return
    
    # Validate required arguments for non-interactive mode
    if not args.layout:
        print("Error: --layout is required unless using --interactive")
        parser.print_help()
        sys.exit(1)
    
    if args.ports is None:
        # Set default ports based on layout
        args.ports = 24 if args.layout == 'single' else 48
    
    if args.sfp is None:
        # Set default SFP ports based on layout
        args.sfp = 2 if args.layout == 'single' else 6
    
    if not args.output:
        # Set default output filename
        args.output = f"{args.layout}_row_switch_{args.ports}p_{args.sfp}sfp.svg"
    
    # Set theme
    theme = Theme.DARK if args.theme == 'dark' else Theme.LIGHT
    
    # Generate the switch
    generate_switch(args.layout, args.ports, args.sfp, args.output, args.name, theme)

if __name__ == "__main__":
    main()
