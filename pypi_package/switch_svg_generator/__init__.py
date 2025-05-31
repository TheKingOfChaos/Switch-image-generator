"""
Network Switch SVG Generator
===========================

A Python package for generating SVG visualizations of network switches with configurable layouts and port configurations.

Classes:
    SwitchSVGGenerator: Main class for generating switch SVG visualizations
    PortStatus: Enum for port status (UP, DOWN, DISABLED)
    SwitchModel: Enum for switch models (BASIC, ENTERPRISE, DATA_CENTER, STACKABLE)
    Theme: Enum for color themes (DARK, LIGHT)
    PortShape: Enum for port shapes (SQUARE, ROUNDED, CIRCULAR)
    LayoutMode: Enum for switch layout modes (ZIGZAG, SINGLE_ROW)

Usage:
    from switch_svg_generator import SwitchSVGGenerator, PortStatus, SwitchModel, Theme, PortShape, LayoutMode
    
    # Create a basic switch with zigzag layout (default)
    switch = SwitchSVGGenerator(
        num_ports=24,
        output_file="switch.svg"
    )
    switch.save_svg()
    
    # Create a switch with single row layout
    switch = SwitchSVGGenerator(
        num_ports=24,
        output_file="single_row_switch.svg",
        layout_mode=LayoutMode.SINGLE_ROW
    )
    switch.save_svg()
"""

from .core import SwitchSVGGenerator, PortStatus, SwitchModel, Theme, PortShape, LayoutMode
from .single_row import SingleRowSwitchGenerator

__version__ = "0.1.0"
__all__ = [
    "SwitchSVGGenerator",
    "SingleRowSwitchGenerator",
    "PortStatus",
    "SwitchModel",
    "Theme",
    "PortShape",
    "LayoutMode"
]
