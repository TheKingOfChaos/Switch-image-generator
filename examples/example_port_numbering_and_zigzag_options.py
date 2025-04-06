#!/usr/bin/env python3
"""
Example script demonstrating port numbering and zigzag pattern options.

This script creates four different switch configurations:
1. Default: Port numbering starts from 1, first port on top row
2. Start from 0: Port numbering starts from 0, first port on top row
3. First port on bottom: Port numbering starts from 1, first port on bottom row
4. Start from 0, first port on bottom: Port numbering starts from 0, first port on bottom row
"""

import os
import sys
import logging

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the switch generator
from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, PortStatus

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create output directory if it doesn't exist
output_dir = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(output_dir, exist_ok=True)

# Define common parameters for all switches
common_params = {
    'num_ports': 24,
    'sfp_ports': 4,
    'switch_model': SwitchModel.ENTERPRISE,
    'port_vlan_map': {
        # Define some VLAN assignments
        1: 10, 2: 10, 3: 10, 4: 10,  # VLAN 10 (Administration)
        5: 20, 6: 20, 7: 20, 8: 20,  # VLAN 20 (Servere)
        9: 30, 10: 30, 11: 30, 12: 30,  # VLAN 30 (Netværksudstyr)
        13: 40, 14: 40, 15: 40, 16: 40, 17: 40, 18: 40, 19: 40, 20: 40,  # VLAN 40 (Kamera netværk)
        21: 30, 22: 30, 23: 30, 24: 30,  # VLAN 30 (Netværksudstyr)
        # SFP ports
        25: 10, 26: 20, 27: 30, 28: 40,
    },
    'port_status_map': {
        # Set some ports to different statuses
        8: PortStatus.DOWN,
        16: PortStatus.DISABLED,
    }
}

# 1. Default: Port numbering starts from 1, first port on top row
default_switch = SwitchSVGGenerator(
    output_file=os.path.join(output_dir, 'default_port_numbering.svg'),
    port_start_number=1,  # Default
    zigzag_start_position="top",  # Default
    **common_params
)
default_switch.save_svg()
print(f"Generated switch with default options: {default_switch.output_file}")

# 2. Start from 0: Port numbering starts from 0, first port on top row
start_from_0_switch = SwitchSVGGenerator(
    output_file=os.path.join(output_dir, 'start_from_0.svg'),
    port_start_number=0,  # Start from 0
    zigzag_start_position="top",  # Default
    **common_params
)
start_from_0_switch.save_svg()
print(f"Generated switch starting from 0: {start_from_0_switch.output_file}")

# 3. First port on bottom: Port numbering starts from 1, first port on bottom row
first_port_bottom_switch = SwitchSVGGenerator(
    output_file=os.path.join(output_dir, 'first_port_bottom.svg'),
    port_start_number=1,  # Default
    zigzag_start_position="bottom",  # First port on bottom
    **common_params
)
first_port_bottom_switch.save_svg()
print(f"Generated switch with first port on bottom: {first_port_bottom_switch.output_file}")

# 4. Start from 0, first port on bottom: Port numbering starts from 0, first port on bottom row
start_0_bottom_switch = SwitchSVGGenerator(
    output_file=os.path.join(output_dir, 'start_0_bottom.svg'),
    port_start_number=0,  # Start from 0
    zigzag_start_position="bottom",  # First port on bottom
    **common_params
)
start_0_bottom_switch.save_svg()
print(f"Generated switch starting from 0 with first port on bottom: {start_0_bottom_switch.output_file}")

print("\nAll SVG files have been generated in the 'output' directory.")
print("You can open them in a web browser to view the different port numbering and zigzag pattern options.")
