#!/usr/bin/env python3
"""
Network Switch SVG Generator - CLI Module
----------------------------
This module provides command-line interface for the switch SVG generator.
"""

import argparse
import sys
import os
from typing import Dict, Optional, List, Any
import logging

from .core import SwitchSVGGenerator, PortStatus, SwitchModel, Theme, PortShape
from .single_row import SingleRowSwitchGenerator


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a network switch SVG with configurable layout."
    )
    
    # Layout options
    parser.add_argument(
        "--layout",
        choices=["single", "double", "sfp-only"],
        help="Layout type: single for one row, double for two rows (zigzag), sfp-only for SFP ports only",
    )
    
    # Port options
    parser.add_argument(
        "--ports",
        type=int,
        help="Number of normal ports",
    )
    
    parser.add_argument(
        "--sfp",
        type=int,
        help="Number of SFP ports",
    )
    
    # Output options
    parser.add_argument(
        "--output",
        help="Output SVG filename",
    )
    
    # Switch options
    parser.add_argument(
        "--name",
        help="Custom switch name",
    )
    
    parser.add_argument(
        "--theme",
        choices=["dark", "light"],
        help="Color theme (default: dark)",
    )
    
    # Interactive mode
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode (prompts for input)",
    )
    
    return parser.parse_args()


def interactive_mode() -> Dict[str, Any]:
    """Run in interactive mode, prompting the user for input."""
    print("=== Switch SVG Generator - Interactive Mode ===")
    
    # Layout selection
    print("\nSelect layout type:")
    print("1. Single row (up to 24 ports)")
    print("2. Double row/zigzag (up to 48 ports)")
    print("3. SFP-only (4-32 SFP ports)")
    
    layout_choice = ""
    while layout_choice not in ["1", "2", "3"]:
        layout_choice = input("Enter choice (1-3): ")
    
    layout_map = {
        "1": "single",
        "2": "double",
        "3": "sfp-only"
    }
    layout = layout_map[layout_choice]
    
    # Port configuration
    if layout == "sfp-only":
        num_ports = 0
        while True:
            try:
                sfp_ports = int(input("\nEnter number of SFP ports (4-32): "))
                if 4 <= sfp_ports <= 32:
                    break
                print("Number of SFP ports must be between 4 and 32.")
            except ValueError:
                print("Please enter a valid number.")
    else:
        max_ports = 24 if layout == "single" else 48
        while True:
            try:
                num_ports = int(input(f"\nEnter number of normal ports (1-{max_ports}): "))
                if 1 <= num_ports <= max_ports:
                    break
                print(f"Number of ports must be between 1 and {max_ports}.")
            except ValueError:
                print("Please enter a valid number.")
        
        max_sfp = 2 if layout == "single" else 6
        while True:
            try:
                sfp_ports = int(input(f"\nEnter number of SFP ports (0-{max_sfp}): "))
                if 0 <= sfp_ports <= max_sfp:
                    break
                print(f"Number of SFP ports must be between 0 and {max_sfp}.")
            except ValueError:
                print("Please enter a valid number.")
    
    # Theme selection
    print("\nSelect theme:")
    print("1. Dark")
    print("2. Light")
    
    theme_choice = ""
    while theme_choice not in ["1", "2"]:
        theme_choice = input("Enter choice (1-2): ")
    
    theme = "dark" if theme_choice == "1" else "light"
    
    # Output file
    default_output = f"{layout}_switch.svg"
    output_file = input(f"\nEnter output filename (default: {default_output}): ")
    if not output_file:
        output_file = default_output
    
    # Switch name
    switch_name = input("\nEnter custom switch name (optional): ")
    
    return {
        "layout": layout,
        "num_ports": num_ports,
        "sfp_ports": sfp_ports,
        "theme": theme,
        "output_file": output_file,
        "switch_name": switch_name
    }


def create_switch(
    layout: str,
    num_ports: int,
    sfp_ports: int,
    output_file: str,
    switch_name: str = "",
    theme: str = "dark"
) -> None:
    """Create a switch SVG based on the specified parameters."""
    # Convert theme string to Theme enum
    theme_enum = Theme.DARK if theme == "dark" else Theme.LIGHT
    
    if layout == "single":
        # Create a single row switch
        switch = SingleRowSwitchGenerator(
            num_ports=num_ports,
            sfp_ports=sfp_ports,
            output_file=output_file,
            switch_name=switch_name,
            theme=theme_enum
        )
    elif layout == "double":
        # Create a double row (zigzag) switch
        switch = SwitchSVGGenerator(
            num_ports=num_ports,
            sfp_ports=sfp_ports,
            output_file=output_file,
            switch_name=switch_name,
            theme=theme_enum
        )
    elif layout == "sfp-only":
        # Create an SFP-only switch
        switch = SwitchSVGGenerator(
            num_ports=0,
            sfp_ports=sfp_ports,
            sfp_only_mode=True,
            output_file=output_file,
            switch_name=switch_name,
            theme=theme_enum
        )
    else:
        raise ValueError(f"Invalid layout: {layout}")
    
    # Generate and save the SVG
    switch.save_svg()
    
    # Also preview the SVG
    switch.preview_svg()
    
    print(f"Switch SVG generated as '{output_file}'")


def main() -> None:
    """Main entry point for the CLI."""
    args = parse_args()
    
    # If interactive mode is enabled, prompt for input
    if args.interactive:
        params = interactive_mode()
    else:
        # Validate required arguments
        if not args.layout:
            print("Error: --layout is required")
            sys.exit(1)
        
        if args.layout != "sfp-only" and not args.ports:
            print("Error: --ports is required for non-SFP-only layouts")
            sys.exit(1)
        
        if not args.sfp:
            print("Error: --sfp is required")
            sys.exit(1)
        
        # Set default output file if not specified
        output_file = args.output or f"{args.layout}_switch.svg"
        
        params = {
            "layout": args.layout,
            "num_ports": args.ports or 0,
            "sfp_ports": args.sfp,
            "theme": args.theme or "dark",
            "output_file": output_file,
            "switch_name": args.name or ""
        }
    
    # Create the switch
    create_switch(**params)


if __name__ == "__main__":
    main()
