#!/usr/bin/env python3
"""
Test script to verify that all ports use VLAN colors regardless of status in the PyPI package.
This script creates a switch with ports in different statuses and VLANs
to demonstrate that port colors are always determined by VLAN assignment.
"""

import sys
import os

# Add the PyPI package directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../pypi_package')))

from switch_svg_generator.core import SwitchSVGGenerator
from switch_svg_generator.core_base import PortStatus, SwitchModel, Theme

# Create a switch with 24 regular ports and 4 SFP ports
generator = SwitchSVGGenerator(
    num_ports=24,
    sfp_ports=4,
    switch_name="PyPI VLAN Colors Test Switch",
    switch_model=SwitchModel.ENTERPRISE,
    output_file="tests/output/pypi_vlan_colors_test.svg",
    # Set different VLANs for ports
    port_vlan_map={
        1: 1,    # VLAN 1 (blue)
        2: 10,   # VLAN 10 (green)
        3: 20,   # VLAN 20 (red)
        4: 30,   # VLAN 30 (orange)
        5: 40,   # VLAN 40 (purple)
        6: 50,   # VLAN 50 (turquoise)
        7: 100,  # VLAN 100 (dark blue)
        8: 200,  # VLAN 200 (gray)
        # SFP ports
        25: 1,   # VLAN 1 (blue)
        26: 10,  # VLAN 10 (green)
        27: 20,  # VLAN 20 (red)
        28: 30,  # VLAN 30 (orange)
    },
    # Set different statuses for ports
    port_status_map={
        # Regular ports with different statuses
        1: PortStatus.UP,
        2: PortStatus.DOWN,
        3: PortStatus.DISABLED,
        4: PortStatus.UP,
        5: PortStatus.DOWN,
        6: PortStatus.DISABLED,
        7: PortStatus.UP,
        8: PortStatus.DOWN,
        # SFP ports with different statuses
        25: PortStatus.UP,
        26: PortStatus.DOWN,
        27: PortStatus.DISABLED,
        28: PortStatus.UP,
    },
    # Set custom labels for the ports
    port_labels={
        1: "UP-1",
        2: "DOWN-10",
        3: "DIS-20",
        4: "UP-30",
        5: "DOWN-40",
        6: "DIS-50",
        7: "UP-100",
        8: "DOWN-200",
        25: "SFP-1",
        26: "SFP-10",
        27: "SFP-20",
        28: "SFP-30",
    }
)

# Generate and save the SVG
generator.save_svg()
print(f"SVG saved to tests/output/pypi_vlan_colors_test.svg")

# Preview the SVG in the default web browser
generator.preview_svg()
