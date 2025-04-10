#!/usr/bin/env python3
"""
Test script to verify SFP port status indicators in the PyPI package.
This script creates a switch with both regular ports and SFP ports,
with different statuses to demonstrate that status indicators
are now visible for all SFP ports regardless of status.
"""

import sys
import os

# Add the PyPI package directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../pypi_package')))

from switch_svg_generator.core import SwitchSVGGenerator
from switch_svg_generator.core_base import PortStatus, SwitchModel, Theme

# Create a switch with 24 regular ports and 4 SFP ports
# Set different statuses for the SFP ports to demonstrate the status indicators
generator = SwitchSVGGenerator(
    num_ports=24,
    sfp_ports=4,
    switch_name="PyPI SFP Status Test Switch",
    switch_model=SwitchModel.ENTERPRISE,
    output_file="tests/output/pypi_sfp_status_test.svg",
    # Set different statuses for the SFP ports
    port_status_map={
        25: PortStatus.UP,       # First SFP port - UP (green)
        26: PortStatus.DOWN,     # Second SFP port - DOWN (red)
        27: PortStatus.DISABLED, # Third SFP port - DISABLED (gray)
        28: PortStatus.UP        # Fourth SFP port - UP (green)
    },
    # Set custom labels for the SFP ports
    port_labels={
        25: "UP",
        26: "DOWN",
        27: "DIS",
        28: "UP"
    }
)

# Generate and save the SVG
generator.save_svg()
print(f"SVG saved to tests/output/pypi_sfp_status_test.svg")

# Preview the SVG in the default web browser
generator.preview_svg()
