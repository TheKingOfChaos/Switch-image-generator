#!/usr/bin/env python3
"""
Configurable Switch Generator
----------------------------
This script allows you to generate a network switch SVG with configurable layout:
1. One row with up to 24 normal ports and 2 SFP ports
2. Two rows with up to 48 normal ports and 6 SFP ports
3. SFP-only mode with 4-32 SFP ports and no regular ports

Usage:
  python3 configurable_switch_generator.py --layout single --ports 24 --sfp 2
  python3 configurable_switch_generator.py --layout double --ports 48 --sfp 6
  python3 configurable_switch_generator.py --layout sfp-only --sfp 8
  python3 configurable_switch_generator.py --interactive
"""

import argparse
import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.dirname(current_dir))  # Add parent directory too

# Try different import approaches to handle both direct and relative imports
try:
    # Try direct import first (when run from project root)
    from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus, LayoutMode
except ImportError:
    try:
        # Try relative import (when run as a module)
        from switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus, LayoutMode
    except ImportError:
        # Last resort - absolute import (when src is in path)
        from switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus, LayoutMode

def generate_switch(layout_type, num_ports, sfp_ports, output_file, switch_name=None, theme=Theme.DARK):
    """
    Generate a switch SVG based on the specified layout type and configuration.
    
    Args:
        layout_type: 'single' for single row, 'double' for double row (zigzag), 'sfp-only' for SFP-only mode
        num_ports: Number of normal ports (ignored in sfp-only mode)
        sfp_ports: Number of SFP ports
        output_file: Output SVG filename
        switch_name: Custom name for the switch (optional)
        theme: Color theme (optional)
    """
    # Validate inputs
    if layout_type == 'sfp-only':
        # SFP-only mode validation
        if sfp_ports < 4 or sfp_ports > 32:
            print(f"Warning: SFP-only mode supports 4-32 SFP ports. Adjusting to valid range.")
            sfp_ports = max(4, min(sfp_ports, 32))
        
        # Set default switch name if not provided
        if not switch_name:
            switch_name = f"{sfp_ports}-Port SFP Switch"
        
        # Create SFP port labels
        port_labels = {}
        for i in range(sfp_ports):
            port_labels[i + 1] = f"SFP{i+1}"
        
        # Create SFP-only switch
        switch = SwitchSVGGenerator(
            sfp_ports=sfp_ports,
            sfp_only_mode=True,  # Enable SFP-only mode
            sfp_layout="zigzag",  # Default to zigzag layout
            switch_width=max(800, 30 + (sfp_ports * 22) + 30),  # Dynamic width based on ports
            switch_height=200,
            switch_model=SwitchModel.ENTERPRISE,
            switch_name=switch_name,
            output_file=output_file,
            theme=theme,
            port_labels=port_labels
        )
    elif layout_type == 'single':
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
        switch = SwitchSVGGenerator(
            num_ports=num_ports,
            switch_width=max(800, 30 + (num_ports * 32) + (sfp_ports * 44) + 30),  # Dynamic width based on ports
            switch_height=180,
            switch_model=SwitchModel.ENTERPRISE,
            switch_name=switch_name,
            sfp_ports=sfp_ports,
            output_file=output_file,
            theme=theme,
            port_labels=port_labels,
            layout_mode=LayoutMode.SINGLE_ROW  # Use single row layout
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
            theme=theme,
            port_labels=port_labels,
            layout_mode=LayoutMode.ZIGZAG  # Use zigzag layout
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
        layout_choice = input("Select layout type (1=Single Row, 2=Double Row, 3=SFP-Only): ").strip()
        if layout_choice in ['1', '2', '3']:
            break
        print("Invalid choice. Please enter 1, 2, or 3.")
    
    if layout_choice == '1':
        layout_type = 'single'
    elif layout_choice == '2':
        layout_type = 'double'
    else:
        layout_type = 'sfp-only'
    
    # For SFP-only mode, we don't need to prompt for normal ports
    if layout_type == 'sfp-only':
        num_ports = 0
        
        # Prompt for number of SFP ports
        while True:
            try:
                sfp_ports = int(input("Number of SFP ports (4-32): ").strip())
                if 4 <= sfp_ports <= 32:
                    break
                print("Invalid number. Please enter a value between 4 and 32.")
            except ValueError:
                print("Please enter a valid number.")
    else:
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
    if layout_type == 'sfp-only':
        default_filename = f"sfp_only_switch_{sfp_ports}p.svg"
    else:
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
    parser.add_argument('--layout', choices=['single', 'double', 'sfp-only'], 
                        help='Layout type: single for one row, double for two rows (zigzag), sfp-only for SFP ports only')
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
    
    if args.layout == 'sfp-only':
        # For SFP-only mode, we don't need normal ports
        args.ports = 0
        
        if args.sfp is None:
            # Default to 8 SFP ports for SFP-only mode
            args.sfp = 8
        
        if not args.output:
            # Set default output filename for SFP-only mode
            args.output = f"sfp_only_switch_{args.sfp}p.svg"
    else:
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
