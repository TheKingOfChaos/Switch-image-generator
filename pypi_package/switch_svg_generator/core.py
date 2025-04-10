#!/usr/bin/env python3
"""
Network Switch SVG Generator
----------------------------
This module generates an SVG image of a network switch with configurable ports.
Port colors can be set based on VLAN assignments, and ports can have different
statuses (up/down/disabled).
"""

import os
import sys
import webbrowser
from enum import Enum
from typing import Dict, List, Tuple, Optional, Union, Set, Any
import logging
from PIL import Image, ImageDraw, ImageFont

# Import methods from other modules
from .core_dimensions import calculate_dimensions
from .core_svg import generate_svg, generate_svg_header, generate_switch_body, generate_switch_details, generate_status_indicators
from .core_ports import generate_ports
from .core_legend import generate_legend

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('switch_svg_generator')


class PortStatus(Enum):
    """Enum representing the status of a switch port."""
    UP = "up"
    DOWN = "down"
    DISABLED = "disabled"


class SwitchModel(Enum):
    """Enum representing different switch models."""
    BASIC = "basic"
    ENTERPRISE = "enterprise"
    DATA_CENTER = "data_center"
    STACKABLE = "stackable"


class Theme(Enum):
    """Enum representing different theme options."""
    DARK = "dark"
    LIGHT = "light"


class PortShape(Enum):
    """Enum representing different port shape options."""
    SQUARE = "square"
    ROUNDED = "rounded"
    CIRCULAR = "circular"


class SwitchSVGGenerator:
    """Class to generate SVG representations of network switches with colored ports."""

    # Default VLAN colors
    DEFAULT_VLAN_COLORS = {
        1: "#3498db",    # Default VLAN - Blue
        10: "#2ecc71",   # Green
        20: "#e74c3c",   # Red
        30: "#f39c12",   # Orange
        40: "#9b59b6",   # Purple
        50: "#1abc9c",   # Turquoise
        100: "#34495e",  # Dark blue
        200: "#7f8c8d",  # Gray
    }

    # Status colors
    STATUS_COLORS = {
        "up": "#2ecc71",       # Green
        "down": "#e74c3c",     # Red
        "disabled": "#7f8c8d", # Gray
    }

    # Theme colors
    THEME_COLORS = {
        Theme.DARK: {
            "background": "#2c3e50",
            "border": "#34495e",
            "text": "#ffffff",
        },
        Theme.LIGHT: {
            "background": "#d3d3d3",  # Light gray background
            "border": "#bdc3c7",
            "text": "#000000",  # Black text
        }
    }

    def __init__(
        self,
        num_ports: int = 24,
        switch_width: int = 800,
        switch_height: int = 130,
        port_width: int = 28,
        port_height: int = 28,
        port_spacing: int = 4,
        legend_spacing: int = 20,
        legend_items_spacing: int = 8,
        legend_item_padding: int = 3,
        vlan_colors: Optional[Dict[int, str]] = None,
        port_vlan_map: Optional[Dict[int, int]] = None,
        port_status_map: Optional[Dict[int, PortStatus]] = None,
        port_labels: Optional[Dict[int, str]] = None,
        output_file: str = "switch.svg",
        switch_model: SwitchModel = SwitchModel.BASIC,
        model_name: str = "",
        switch_name: str = "",
        theme: Theme = Theme.LIGHT,
        port_shape: PortShape = PortShape.SQUARE,
        show_status_indicator: bool = True,
        sfp_ports: int = 0,
        sfp_layout: str = "zigzag",
        sfp_group_size: int = 0,
        switch_body_color: Optional[str] = None,
        switch_body_border_color: str = "#000000",
        switch_body_border_width: int = 2,
        port_group_size: int = 0,
        port_group_spacing: int = 7,
        sfp_only_mode: bool = False,
        port_start_number: int = 1,
        zigzag_start_position: str = "top",
    ):
        """Initialize the switch SVG generator with configuration parameters."""
        # Validate inputs based on mode
        self.sfp_only_mode = sfp_only_mode
        
        # Validate port_start_number
        if port_start_number not in [0, 1]:
            raise ValueError("port_start_number must be either 0 or 1")
        self.port_start_number = port_start_number
        
        # Validate zigzag_start_position
        if zigzag_start_position not in ["top", "bottom"]:
            raise ValueError("zigzag_start_position must be either 'top' or 'bottom'")
        self.zigzag_start_position = zigzag_start_position
        
        if sfp_only_mode:
            # In SFP-only mode, validate SFP ports
            if not 4 <= sfp_ports <= 32:
                raise ValueError("In SFP-only mode, number of SFP ports must be between 4 and 32")
            # Set num_ports to 0 since we're not using regular ports
            self.num_ports = 0
        else:
            # Normal mode validation
            if not 5 <= num_ports <= 48:
                raise ValueError("Number of ports must be between 5 and 48")
            if sfp_ports < 0 or sfp_ports > 6:
                raise ValueError("Number of SFP ports must be between 0 and 6")
            self.num_ports = num_ports
        
        if port_group_size < 0:
            raise ValueError("Port group size must be non-negative")
        self.switch_width = max(switch_width, 400)  # Minimum width
        self.switch_height = max(switch_height, 150)  # Minimum height
        self.port_width = max(port_width, 10)  # Minimum port width
        self.port_height = max(port_height, 10)  # Minimum port height
        self.port_spacing = max(port_spacing, 2)  # Minimum spacing
        self.sfp_ports = sfp_ports
        self.sfp_layout = sfp_layout
        self.sfp_group_size = sfp_group_size
        self.port_group_size = port_group_size
        self.port_group_spacing = port_group_spacing
        
        # Use provided VLAN colors or defaults
        self.vlan_colors = vlan_colors or self.DEFAULT_VLAN_COLORS.copy()
        
        # Default port to VLAN mapping (all ports on VLAN 1 by default)
        if sfp_only_mode:
            # In SFP-only mode, only create mappings for SFP ports
            self.port_vlan_map = port_vlan_map or {i: 1 for i in range(self.port_start_number, sfp_ports + self.port_start_number)}
            self.port_status_map = port_status_map or {i: PortStatus.UP for i in range(self.port_start_number, sfp_ports + self.port_start_number)}
        else:
            # Normal mode - create mappings for all ports
            self.port_vlan_map = port_vlan_map or {i: 1 for i in range(self.port_start_number, num_ports + self.port_start_number)}
            self.port_status_map = port_status_map or {i: PortStatus.UP for i in range(self.port_start_number, num_ports + self.port_start_number)}
        
        # Port labels (empty by default)
        self.port_labels = port_labels or {}
        
        self.output_file = output_file
        self.switch_model = switch_model
        self.model_name = model_name or switch_model.value  # Use custom model name or default to enum value
        # Set switch name based on mode
        if sfp_only_mode:
            self.switch_name = switch_name or f"{sfp_ports}-Port SFP Switch"
        else:
            self.switch_name = switch_name or f"{num_ports}-Port Network Switch"
        self.theme = theme
        self.port_shape = port_shape
        self.show_status_indicator = show_status_indicator
        self.legend_spacing = legend_spacing
        self.legend_items_spacing = legend_items_spacing
        self.legend_item_padding = legend_item_padding
        self.switch_body_border_color = switch_body_border_color
        self.switch_body_border_width = switch_body_border_width
        
        # Calculate derived properties
        self.theme_colors = self.THEME_COLORS[theme]
        
        # Set switch body color - if not provided, use a slightly different shade of the background color
        if switch_body_color:
            self.switch_body_color = switch_body_color
        else:
            # For light theme, use a slightly darker shade
            # For dark theme, use a slightly lighter shade
            if self.theme == Theme.LIGHT:
                self.switch_body_color = "#c0c0c0"  # Slightly darker gray for light theme
            else:
                self.switch_body_color = "#3c4e60"  # Slightly lighter for dark theme
        
        # Initialize calculated properties
        self.body_width = 0
        self.actual_body_width = 0
        self.ports_width = 0

    def get_port_color(self, port_num: int) -> str:
        """
        Get the color for a specific port based on its VLAN assignment.
        Always uses VLAN color regardless of port status.
        """
        # Always use VLAN color regardless of status
        vlan_id = self.port_vlan_map.get(port_num, 1)
        return self.vlan_colors.get(vlan_id, self.DEFAULT_VLAN_COLORS[1])

    def get_port_shape_attributes(self) -> Dict[str, Union[int, str]]:
        """Get the SVG attributes for the port shape based on the selected port shape."""
        if self.port_shape == PortShape.SQUARE:
            return {"rx": 0, "ry": 0}
        elif self.port_shape == PortShape.ROUNDED:
            return {"rx": 2, "ry": 2}
        elif self.port_shape == PortShape.CIRCULAR:
            radius = min(self.port_width, self.port_height) // 2
            return {"rx": radius, "ry": radius}
        else:
            return {"rx": 2, "ry": 2}  # Default to rounded

    def get_used_vlans(self) -> Set[int]:
        """Get the set of VLANs that are actually used in the port-VLAN mapping."""
        return set(self.port_vlan_map.values())

    def get_used_statuses(self) -> Set[PortStatus]:
        """Get the set of port statuses that are actually used."""
        return set(self.port_status_map.values())
        
    def get_text_width(self, text: str, font_size: int = 10, font_family: str = "Arial") -> float:
        """Get the width of text in pixels."""
        try:
            # Try to find the font file
            # Common font locations
            font_paths = [
                # Windows font paths
                "C:/Windows/Fonts/arial.ttf",
                # Linux font paths
                "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf",
                "/usr/share/fonts/TTF/arial.ttf",
                # macOS font paths
                "/Library/Fonts/Arial.ttf",
                "/System/Library/Fonts/Supplemental/Arial.ttf"
            ]
            
            # Use the first font file that exists
            font_file = None
            for path in font_paths:
                if os.path.exists(path):
                    font_file = path
                    break
            
            if font_file:
                # Create a font object with the found font file
                font = ImageFont.truetype(font_file, font_size)
            else:
                # Fallback to default font
                font = ImageFont.load_default()
                # Scale default font (which is usually small)
                font_size_ratio = font_size / 10
            
            # Get text dimensions
            # For newer Pillow versions (>=8.0.0)
            if hasattr(font, "getlength"):
                text_width = font.getlength(text)
            # For older Pillow versions
            else:
                text_width = font.getsize(text)[0]
                
            return text_width
        except Exception as e:
            # Log the error
            logger.error(f"Error measuring text width: {e}")
            # Fall back to the approximation method
            return self.approximate_text_width(text, font_size)

    def approximate_text_width(self, text: str, font_size: int = 10) -> float:
        """Approximate text width when Pillow measurement fails."""
        # Character width approximation (improved version)
        char_widths = {
            'i': 2.5, 'l': 2.5, 'I': 3, 'j': 3, 't': 3.5, 'f': 3.5, 'r': 4,
            'a': 5.5, 'c': 5.5, 'e': 5.5, 'o': 6, 'n': 6, 's': 5, 'u': 6, 'v': 5.5, 'x': 5.5, 'z': 5,
            'b': 6, 'd': 6, 'g': 6, 'h': 6, 'k': 5.5, 'p': 6, 'q': 6, 'y': 5.5,
            'm': 9, 'w': 8.5, 'A': 7, 'B': 7, 'C': 7.5, 'D': 7.5, 'E': 7, 'F': 6.5, 'G': 8,
            'H': 7.5, 'J': 5.5, 'K': 7, 'L': 6, 'N': 7.5, 'O': 8, 'P': 7, 'Q': 8, 'R': 7.5,
            'S': 7, 'T': 6.5, 'U': 7.5, 'V': 7, 'W': 10, 'X': 7, 'Y': 7, 'Z': 6.5,
            '0': 6, '1': 6, '2': 6, '3': 6, '4': 6, '5': 6, '6': 6, '7': 6, '8': 6, '9': 6,
            '.': 3, ',': 3, ':': 3, ';': 3, ' ': 3, '-': 4, '_': 6, '/': 3, '\\': 3,
            '(': 4, ')': 4, '[': 4, ']': 4, '{': 4, '}': 4
        }
        
        # Default width for characters not in the mapping
        default_width = 6
        
        # Calculate total width
        total_width = sum(char_widths.get(c, default_width) for c in text)
        
        # Scale by font size ratio (assuming the mapping is for 10px)
        return total_width * (font_size / 10)

    # Import methods from other modules
    calculate_dimensions = calculate_dimensions
    generate_svg = generate_svg
    generate_svg_header = generate_svg_header
    generate_switch_body = generate_switch_body
    generate_switch_details = generate_switch_details
    generate_status_indicators = generate_status_indicators
    generate_ports = generate_ports
    generate_legend = generate_legend

    def save_svg(self) -> None:
        """Generate the SVG and save it to the output file."""
        svg_content = self.generate_svg()
        
        # Fix any issues with angle brackets in the SVG content
        # Check if the XML declaration and SVG opening tag have angle brackets
        if not svg_content.startswith('<?xml'):
            # If it starts with 'xml' without the opening angle bracket, add it
            if svg_content.startswith('xml'):
                svg_content = '<' + svg_content
        
        # Check if the SVG tag is missing its opening angle bracket
        # Look for 'svg width=' without the opening angle bracket
        if 'svg width="' in svg_content and '<svg width="' not in svg_content:
            # Add the opening angle bracket before 'svg'
            svg_content = svg_content.replace('svg width="', '<svg width="', 1)
        
        # Check for double angle brackets (<<svg)
        if '<<svg' in svg_content:
            # Replace <<svg with <svg
            svg_content = svg_content.replace('<<svg', '<svg', 1)
        
        try:
            with open(self.output_file, 'w') as f:
                f.write(svg_content)
            
            logger.info(f"SVG switch diagram saved to {self.output_file}")
        except IOError as e:
            logger.error(f"Error saving SVG to {self.output_file}: {e}")
            raise

    def preview_svg(self) -> None:
        """Generate the SVG, save it, and open it in the default web browser."""
        self.save_svg()
        
        try:
            abs_path = os.path.abspath(self.output_file)
            file_url = f"file://{abs_path}"
            
            logger.info(f"Opening SVG in browser: {file_url}")
            webbrowser.open(file_url)
        except Exception as e:
            logger.error(f"Error opening SVG in browser: {e}")
            raise
