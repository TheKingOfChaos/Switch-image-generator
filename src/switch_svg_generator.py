#!/usr/bin/env python3
"""
Network Switch SVG Generator
----------------------------
This script generates an SVG image of a network switch with configurable ports.
Port colors can be set based on VLAN assignments, and ports can have different
statuses (up/down/disabled).

Features:
- Configurable number of ports
- VLAN-based port coloring
- Port status indicators
- Support for different switch models
- Customizable port labels
- Dark/light theme support
- Optional SFP ports
"""

import argparse
import os
import sys
import webbrowser
from enum import Enum
from typing import Dict, List, Tuple, Optional, Union, Set, Any
import logging
from PIL import Image, ImageDraw, ImageFont


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


class LayoutMode(Enum):
    """Enum representing different port layout options."""
    ZIGZAG = "zigzag"
    SINGLE_ROW = "single_row"


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
        PortStatus.UP: "#2ecc71",       # Green
        PortStatus.DOWN: "#e74c3c",     # Red
        PortStatus.DISABLED: "#7f8c8d", # Gray
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
        switch_height: int = 130,  # Changed from 200 to 130 for consistent dimensions
        port_width: int = 28,
        port_height: int = 28,
        port_spacing: int = 4,
        legend_spacing: int = 20,  # Spacing between switch body and legend title
        legend_items_spacing: int = 8,  # Spacing between legend title and legend items
        legend_item_padding: int = 3,  # Padding between legend items (horizontal spacing)
        legend_row_offset: int = 20,  # Offset for legend rows
        vlan_colors: Optional[Dict[int, str]] = None,
        port_vlan_map: Optional[Dict[int, int]] = None,
        port_status_map: Optional[Dict[int, PortStatus]] = None,
        port_labels: Optional[Dict[int, str]] = None,
        output_file: str = "switch.svg",
        switch_model: SwitchModel = SwitchModel.BASIC,
        model_name: str = "",  # Custom model name to display on the switch
        switch_name: str = "",
        theme: Theme = Theme.LIGHT,
        port_shape: PortShape = PortShape.SQUARE,
        show_status_indicator: bool = True,
        sfp_ports: int = 0,  # Number of SFP ports (0-6 in normal mode, 4-32 in SFP-only mode)
        sfp_layout: str = "zigzag",  # Options: "horizontal" or "zigzag"
        sfp_group_size: int = 0,  # Number of SFP ports per group (0 means no grouping)
        switch_body_color: Optional[str] = None,  # Custom color for the switch body
        switch_body_border_color: str = "#000000",  # Border color for the switch body (default: black)
        switch_body_border_width: int = 2,  # Border width for the switch body
        port_group_size: int = 0,  # Number of ports per group (0 means no grouping)
        port_group_spacing: int = 7,  # Additional spacing between port groups in pixels
        sfp_only_mode: bool = False,  # When True, creates a switch with only SFP ports
        port_start_number: int = 1,  # Starting port number (0 or 1)
        zigzag_start_position: str = "top",  # First port position in zigzag pattern ("top" or "bottom")
        layout_mode: LayoutMode = LayoutMode.ZIGZAG,  # Port layout mode (zigzag or single row)
    ):
        """
        Initialize the switch SVG generator.
        
        Args:
            num_ports: Number of ports on the switch
            switch_width: Width of the switch in pixels
            switch_height: Height of the switch in pixels
            port_width: Width of each port in pixels
            port_height: Height of each port in pixels
            port_spacing: Spacing between ports in pixels
            vlan_colors: Dictionary mapping VLAN IDs to color codes
            port_vlan_map: Dictionary mapping port numbers to VLAN IDs
            port_status_map: Dictionary mapping port numbers to their status
            port_labels: Dictionary mapping port numbers to custom labels
            output_file: Path to save the SVG file
            switch_model: The model of the switch to render
            switch_name: Custom name for the switch
            theme: Color theme to use (dark or light)
            port_shape: Shape of the ports (square, rounded, circular)
            show_status_indicator: Whether to show port status indicators
            sfp_ports: Number of SFP ports to add (0-6 in normal mode, 4-32 in SFP-only mode)
            sfp_only_mode: When True, creates a switch with only SFP ports (no regular ports)
            port_start_number: Starting port number (0 or 1)
            zigzag_start_position: First port position in zigzag pattern ("top" or "bottom")
            legend_row_offset: Offset for legend rows
        """
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
        self.legend_row_offset = legend_row_offset
        
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
                
        # Store the layout mode
        self.layout_mode = layout_mode

    def get_port_color(self, port_num: int) -> str:
        """
        Get the color for a specific port based on its VLAN assignment.
        Always uses VLAN color regardless of port status.
        
        Args:
            port_num: The port number
            
        Returns:
            A color code string
        """
        # Always use VLAN color regardless of status
        vlan_id = self.port_vlan_map.get(port_num, 1)
        return self.vlan_colors.get(vlan_id, self.DEFAULT_VLAN_COLORS[1])

    def get_port_shape_attributes(self) -> Dict[str, Union[int, str]]:
        """
        Get the SVG attributes for the port shape based on the selected port shape.
        
        Returns:
            Dictionary of shape attributes
        """
        if self.port_shape == PortShape.SQUARE:
            return {"rx": 0, "ry": 0}
        elif self.port_shape == PortShape.ROUNDED:
            return {"rx": 2, "ry": 2}
        elif self.port_shape == PortShape.CIRCULAR:
            # For circular, we'll use the minimum of width and height
            radius = min(self.port_width, self.port_height) // 2
            return {"rx": radius, "ry": radius}
        else:
            return {"rx": 2, "ry": 2}  # Default to rounded

    def get_used_vlans(self) -> Set[int]:
        """
        Get the set of VLANs that are actually used in the port-VLAN mapping.
        
        Returns:
            Set of VLAN IDs
        """
        return set(self.port_vlan_map.values())

    def get_used_statuses(self) -> Set[PortStatus]:
        """
        Get the set of port statuses that are actually used.
        
        Returns:
            Set of PortStatus values
        """
        return set(self.port_status_map.values())
        
    def get_text_width(self, text: str, font_size: int = 10, font_family: str = "Arial") -> float:
        """
        Get the exact width of text in pixels using Pillow.
        
        Args:
            text: The text to measure
            font_size: Font size in pixels
            font_family: Font family name
            
        Returns:
            Width of the text in pixels
        """
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
        """
        Approximate text width when Pillow measurement fails.
        
        Args:
            text: The text to measure
            font_size: Font size in pixels
            
        Returns:
            Approximated width of the text in pixels
        """
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

    def calculate_dimensions(self) -> Tuple[int, int, int, int]:
        """
        Calculate the dimensions for the switch and port layout.
        
        Returns:
            Tuple of (adjusted_width, adjusted_height, ports_per_row, num_rows)
        """
        # Calculate port positioning
        if self.sfp_only_mode:
            # In SFP-only mode, there are no regular ports
            ports_per_row = 0
            num_rows = 0
            ports_height = 0
        else:
            # Normal mode - calculate regular port layout based on layout mode
            if self.layout_mode == LayoutMode.SINGLE_ROW:
                # Single row layout - all ports in one row
                ports_per_row = self.num_ports
                num_rows = 1
            else:  # ZIGZAG layout
                ports_per_row = min(self.num_ports, 24)  # Use 24 ports per row max
                num_rows = (self.num_ports + ports_per_row - 1) // ports_per_row
                
                # For zigzag pattern, we need half as many rows (rounded up)
                if self.num_ports > 1:
                    num_rows = (self.num_ports + 1) // 2  # Ceiling division for odd number of ports
            
            # Calculate space needed for ports
            row_spacing = 4  # Reduced from 6px to 4px for more compact layout
            ports_height = num_rows * (self.port_height + row_spacing)
        
        # Calculate space needed for header (switch name, model, etc.)
        header_height = 40  # Reduced from 50
        if self.switch_model != SwitchModel.BASIC:
            header_height += 10  # Reduced from 15
        
        # Calculate space needed for legend (at least 20px, more if many VLANs)
        legend_height = max(20, 12 * (len(self.get_used_vlans()) // 4 + 1))
        # Always add space for SFP ports in the legend height calculation
        # This ensures consistent height even for switches without SFP ports
        legend_height += 20
        
        # Add extra space between ports and legend
        spacing_between_ports_and_legend = 10  # Reduced from 15
        
        # Define spacing constants
        start_spacing = 30  # Space from start of switch to first port (actual spacing is 20px from edge)
        left_edge_spacing = 20  # Actual spacing from left edge to first port
        end_spacing = left_edge_spacing  # Space from last port to right edge (matching left spacing)
        sfp_spacing = 20    # Space between last regular port and first SFP port (not used in SFP-only mode)
        
        # Calculate dimensions based on mode
        if self.sfp_only_mode:
            # In SFP-only mode, there are no regular ports
            regular_port_columns = 0
            regular_ports_width = 0
            port_grouping_extra_width = 0
        else:
            # Normal mode - calculate regular port layout
            # For zigzag pattern, we need half as many columns
            regular_port_columns = (self.num_ports + 1) // 2  # Ceiling division for odd number of ports
            
            # Calculate width needed for port grouping if enabled
            port_grouping_extra_width = 0
            if self.port_group_size > 0 and regular_port_columns > 0:
                # Calculate how many groups we have
                num_groups = (regular_port_columns + self.port_group_size - 1) // self.port_group_size
                # Calculate extra spacing from grouping
                port_grouping_extra_width = (num_groups - 1) * self.port_group_spacing if num_groups > 1 else 0
            
            # Calculate width needed for the actual number of ports
            # For regular ports, we need columns * (width + spacing)
            regular_ports_width = (regular_port_columns * (self.port_width + self.port_spacing)) + port_grouping_extra_width
        
        # Calculate how many columns we need for SFP ports
        sfp_columns = (self.sfp_ports + 1) // 2  # Ceiling division to get number of columns
        
        # For SFP ports, calculate width based on layout
        if self.sfp_layout == "horizontal":
            # For horizontal layout, all SFP ports are in a single row
            sfp_ports_width = self.sfp_ports * 40  # Each SFP port is 40px wide
            sfp_ports_width += (self.sfp_ports - 1) * self.port_spacing  # Add spacing between ports
            
            # Add extra spacing for SFP port grouping if enabled
            if self.sfp_group_size > 0 and self.sfp_ports > 1:
                sfp_groups = (self.sfp_ports + self.sfp_group_size - 1) // self.sfp_group_size
                sfp_ports_width += (sfp_groups - 1) * self.port_group_spacing
        else:
            # For vertical or zigzag layout
            if self.sfp_ports <= 2:
                # SFP ports are arranged vertically (one below the other)
                sfp_ports_width = 40  # Just one column width
            else:
                # SFP ports are arranged in zigzag pattern
                sfp_ports_width = (sfp_columns * 40) + ((sfp_columns - 1) * self.port_spacing)
        
        # Calculate the position of the last port
        if self.sfp_only_mode:
            # In SFP-only mode, the first port is the first SFP port
            last_port_x = start_spacing
            last_port_width = sfp_ports_width  # Total width of SFP ports
        elif self.sfp_ports > 0:
            # If there are SFP ports in normal mode, the last port is the last SFP port
            last_port_x = start_spacing + regular_ports_width + sfp_spacing
            last_port_width = sfp_ports_width  # Total width of SFP ports
        else:
            # If there are no SFP ports, the last port is the last regular port
            last_port_x = start_spacing + regular_ports_width - self.port_spacing
            last_port_width = self.port_width
        
        # Calculate the width needed for the switch body with equal spacing on both sides
        # Left spacing = start_spacing - 10 = 20px (from left edge to first port)
        # For equal spacing, right spacing should also be 20px
        # For a 24-port switch with last port at x=382 with width 28px:
        # body_width = (382 + 28 + 20) - 10 = 420px
        
        # The issue is that for regular ports, we're including port_spacing in the calculation
        # of regular_ports_width, but we need to subtract it for the last port
        # This is causing the right spacing to be larger than the left spacing
        
        # Adjust the last_port_x to account for the port spacing
        if self.sfp_ports == 0:
            # If there are no SFP ports, adjust the last port position
            last_port_x = start_spacing + (regular_port_columns - 1) * (self.port_width + self.port_spacing)
        
        body_width = (last_port_x + last_port_width + left_edge_spacing) - 10
        
        # Store the body width for later use
        self.body_width = body_width
        
        # Set the actual width to the body width plus margins
        actual_width = body_width + 20  # Add 20px for margins (10px on each side)
        
        # Store the width needed for ports for later use in port positioning
        self.ports_width = actual_width - start_spacing - end_spacing
        
        # Calculate minimum width based on mode
        if self.sfp_only_mode:
            # In SFP-only mode, minimum is based on 4 SFP ports
            min_sfp_ports = 4
            min_normal_ports = 0  # No normal ports in SFP-only mode
            # For SFP ports in zigzag pattern (2 columns)
            min_sfp_width = start_spacing + (min_sfp_ports // 2) * (40 + self.port_spacing)
            min_normal_width = 0
        else:
            # Normal mode - minimum based on 10 normal ports and 1 SFP port
            min_normal_ports = 10
            min_sfp_ports = 1
            
            # For normal ports in zigzag pattern (5 columns)
            min_normal_width = start_spacing + (min_normal_ports // 2) * (self.port_width + self.port_spacing)
            
            # For SFP ports
            min_sfp_width = sfp_spacing + 40  # 40px is the width of an SFP port
        
        # Calculate minimum actual width
        min_actual_width = min_normal_width + min_sfp_width
        
        # Calculate the minimum body width (without margins)
        min_body_width = min_actual_width
        
        # Use the maximum of the calculated body width and the minimum body width
        body_width = max(body_width, min_body_width)
        
        # Store the body width for later use
        self.body_width = body_width
        
        # Store the actual width needed for the switch body (including margins)
        self.actual_body_width = body_width + 20  # Add 20px for margins (10px on each side)
        
        # Calculate the exact width needed for all ports
        # This ensures there's no extra space between the last SFP port and the right edge
        exact_width = actual_width + 20  # Add 20px for margins (10px on each side)
        
        # Total minimum width with margins
        minimum_width = self.actual_body_width  # Already includes margins
        
        # Use the actual body width (which includes margins) for the SVG width
        # This ensures the canvas width matches the switch body width plus margins
        adjusted_width = self.actual_body_width
        
        # Ensure the adjusted width is at least the minimum width
        if self.sfp_only_mode:
            # For SFP-only mode, ensure minimum width for 4 SFP ports
            if self.sfp_ports < min_sfp_ports:
                # Calculate the minimum width for 4 SFP ports
                min_body_width = min_sfp_width
                min_switch_width = min_body_width + 20  # Add 20px for margins
                
                # Force the width to be exactly the minimum width
                adjusted_width = 280  # Hardcoded width for 4 SFP ports
                
                # Also update the body width to match
                self.body_width = 260  # Hardcoded body width for 4 SFP ports
        else:
            # For normal mode, ensure minimum width for 10 normal ports + 1 SFP
            if self.num_ports < min_normal_ports or (self.num_ports == min_normal_ports and self.sfp_ports < min_sfp_ports):
                # Calculate the minimum width for a 10-port switch with 1 SFP
                # Calculate the exact width needed for a 10-port switch with 1 SFP
                min_body_width = min_normal_width + min_sfp_width
                min_switch_width = min_body_width + 20  # Add 20px for margins
                
                # Force the width to be exactly the minimum width
                adjusted_width = 280  # Hardcoded width for 10 ports + 1 SFP
                
                # Also update the body width to match
                self.body_width = 260  # Hardcoded body width for 10 ports + 1 SFP
        
        # Calculate height needed for SFP ports if any
        sfp_height = 0
        if self.sfp_ports > 0:
            if self.sfp_layout == "horizontal":
                # For horizontal layout, height is just one row
                sfp_height = 40  # 40px height for one row
            else:
                # For zigzag layout, calculate based on number of rows
                sfp_rows = (self.sfp_ports + 1) // 2  # Ceiling division for odd number of ports
                sfp_height = sfp_rows * 40 + (sfp_rows - 1) * 10  # 40px height, 10px spacing
            
            # In SFP-only mode, ports_height is just the SFP height
            # In normal mode, use the maximum of regular ports height and SFP height
            if self.sfp_only_mode:
                ports_height = sfp_height
            else:
                ports_height = max(ports_height, sfp_height)
        
        # Use the provided switch_height for the switch body
        adjusted_height = self.switch_height
        
        # Estimate the number of legend rows needed based on the available width
        # and the number of VLANs and statuses
        num_vlans = len(self.get_used_vlans())
        num_statuses = len(self.get_used_statuses())
        
        # Estimate average width of a legend item (VLAN or status)
        avg_item_width = 150  # pixels
        
        # Calculate how many items can fit in one row
        legend_x = 30  # Left margin for legend
        available_legend_width = self.actual_body_width - 2 * legend_x
        items_per_row = max(1, int(available_legend_width / avg_item_width))
        
        # Calculate how many rows we need for all items
        total_items = num_vlans + num_statuses
        estimated_legend_rows = (total_items + items_per_row - 1) // items_per_row
        
        # Calculate height needed for legend
        # Legend title + spacing + (rows * row_height)
        legend_title_height = 20  # Height of "Legend:" text
        legend_row_height = 25    # Height of each row of legend items
        legend_height = legend_title_height + self.legend_items_spacing + (estimated_legend_rows * legend_row_height)
        
        # Calculate total height needed
        # Switch body + legend spacing + legend height
        calculated_height = self.switch_height + self.legend_spacing + legend_height
        
        # Use the maximum of the calculated height and the minimum height (240px)
        adjusted_height = max(240, calculated_height)
        
        return adjusted_width, adjusted_height, ports_per_row, num_rows

    def generate_svg_header(self, adjusted_width: int, adjusted_height: int) -> List[str]:
        """
        Generate the SVG header content.
        
        Args:
            adjusted_width: The calculated width of the SVG
            adjusted_height: The calculated height of the SVG
            
        Returns:
            List of SVG header lines
        """
        svg = [
            f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
            f'<svg width="{adjusted_width}" height="{adjusted_height}" xmlns="http://www.w3.org/2000/svg">',
            f'  <!-- Network Switch SVG generated by SwitchSVGGenerator -->',
            f'  <!-- {self.num_ports} port switch ({self.switch_model.value}) -->',
            f'  <!-- Generated with theme: {self.theme.value} -->',
            f'  <!-- Background for entire image -->',
            f'  <rect x="0" y="0" width="{adjusted_width}" height="{adjusted_height}" fill="{self.theme_colors["background"]}" />'
        ]
        return svg

    def generate_switch_body(self, adjusted_width: int, adjusted_height: int) -> List[str]:
        """
        Generate the SVG content for the switch body.
        
        Args:
            adjusted_width: The calculated width of the SVG
            adjusted_height: The calculated height of the SVG
            
        Returns:
            List of SVG lines for the switch body
        """
        svg = []
        svg.append(f'  <!-- Switch body -->')
        
        # Use the switch_height for the body height
        body_height = self.switch_height - 20  # -20 for the margins (10px top and bottom)
        
        # Use the body_width calculated in calculate_dimensions
        # This ensures equal spacing on both sides of the switch
        body_width = self.body_width
            
        svg.append(f'  <rect x="10" y="10" width="{body_width}" height="{body_height}" '
                  f'rx="10" ry="10" fill="{self.switch_body_color}" '
                  f'stroke="{self.switch_body_border_color}" stroke-width="{self.switch_body_border_width}" />')
        return svg

    def generate_switch_details(self, adjusted_width: int) -> List[str]:
        """
        Generate the SVG content for the switch details (name, model, etc.).
        
        Args:
            adjusted_width: The calculated width of the SVG
            
        Returns:
            List of SVG lines for the switch details
        """
        svg = []
        svg.append(f'  <!-- Switch details -->')
        svg.append(f'  <text x="30" y="40" font-family="Arial" font-size="16" '
                  f'fill="{self.theme_colors["text"]}">{self.switch_name}</text>')
        
        # Add model info if not basic or if a custom model name is provided
        if self.switch_model != SwitchModel.BASIC or self.model_name != self.switch_model.value:
            svg.append(f'  <text x="30" y="60" font-family="Arial" font-size="12" '
                      f'fill="{self.theme_colors["text"]}">Model: {self.model_name}</text>')
        
        return svg

    def generate_status_indicators(self, adjusted_width: int) -> List[str]:
        """
        Generate the SVG content for the switch status indicators.
        
        Args:
            adjusted_width: The calculated width of the SVG
            
        Returns:
            List of SVG lines for the status indicators
        """
        svg = []
        svg.append(f'  <!-- Status LEDs -->')
        
        # Use the body_width calculated in calculate_dimensions
        # This ensures consistent positioning with the switch body
        body_width = self.body_width
        
        # Position from the right edge of the switch body
        right_edge = 10 + body_width  # 10px left margin + body width
        
        # For small switches (10 or fewer ports), only show the PWR indicator
        is_small_switch = self.num_ports <= 10
        
        # Position the PWR indicator consistently at the right side of the switch body
        # Calculate the width of the PWR text
        pwr_text = "PWR"
        pwr_text_width = self.get_text_width(pwr_text, font_size=12, font_family="Arial")
        
        # Position PWR text near the right edge with consistent margin
        margin_from_edge = 12  # Reduced margin from right edge
        pwr_text_x = right_edge - pwr_text_width - margin_from_edge
        pwr_circle_x = pwr_text_x - 10  # 10px to the left of the text
        
        svg.append(f'  <circle cx="{pwr_circle_x}" cy="30" r="5" fill="#2ecc71" />')
        svg.append(f'  <text x="{pwr_text_x}" y="35" font-family="Arial" '
                  f'font-size="12" fill="{self.theme_colors["text"]}">PWR</text>')
        
        # Only show STATUS and MGMT indicators on larger switches
        if not is_small_switch:
            # Status LED - position relative to PWR
            status_text_width = 50  # Approximate width of "STATUS" text
            status_circle_x = pwr_circle_x - status_text_width - 15  # 15px spacing between indicators
            status_text_x = status_circle_x + 10  # 10px to the right of the circle
            
            svg.append(f'  <circle cx="{status_circle_x}" cy="30" r="5" fill="#f1c40f" />')
            svg.append(f'  <text x="{status_text_x}" y="35" font-family="Arial" '
                      f'font-size="12" fill="{self.theme_colors["text"]}">STATUS</text>')
            
            # Add more indicators for enterprise and data center models - increased spacing
            if self.switch_model in [SwitchModel.ENTERPRISE, SwitchModel.DATA_CENTER]:
                mgmt_text_width = 40  # Approximate width of "MGMT" text
                mgmt_circle_x = status_circle_x - mgmt_text_width - 15  # 15px spacing between indicators
                mgmt_text_x = mgmt_circle_x + 10  # 10px to the right of the circle
                
                svg.append(f'  <circle cx="{mgmt_circle_x}" cy="30" r="5" fill="#3498db" />')
                svg.append(f'  <text x="{mgmt_text_x}" y="35" font-family="Arial" '
                          f'font-size="12" fill="{self.theme_colors["text"]}">MGMT</text>')
        
        return svg

    def generate_legend(self, adjusted_width: int, adjusted_height: int) -> List[str]:
        """
        Generate the SVG content for the VLAN and status legend.
        
        Args:
            adjusted_width: The calculated width of the SVG
            adjusted_height: The calculated height of the SVG
            
        Returns:
            List of SVG lines for the legend
        """
        svg = []
        svg.append(f'  <!-- Legend -->')
        
        # Place legend under the switch
        # Start from the left side, aligned with the switch body
        legend_x = 30  # Align with the switch details
        
        # Calculate the bottom of the switch
        # The switch body starts at y=10 and has a height of (switch_height - 20)
        # So the bottom of the switch is at y=10 + (switch_height - 20) = switch_height - 10
        switch_bottom = 10 + (self.switch_height - 20)
        
        # Position the legend title exactly legend_spacing pixels below the switch bottom
        legend_title_y = switch_bottom + self.legend_spacing
        
        # Add a legend title
        svg.append(f'  <text x="{legend_x}" y="{legend_title_y}" font-family="Arial" '
                  f'font-size="12" font-weight="bold" fill="{self.theme_colors["text"]}">Legend:</text>')
        
        # Position VLAN section title below the legend title with additional 3px spacing
        vlan_section_y = legend_title_y + self.legend_items_spacing + 3  # Added 3px extra spacing
        svg.append(f'  <text x="{legend_x}" y="{vlan_section_y}" font-family="Arial" '
                  f'font-size="11" font-weight="bold" fill="{self.theme_colors["text"]}">VLANs:</text>')
        
        # Position legend items below the VLAN section title
        legend_items_y = vlan_section_y + self.legend_items_spacing
        
        # Debug logging to help diagnose spacing issues
        logger.info(f"Legend spacing: title_y={legend_title_y}, items_y={legend_items_y}, spacing={self.legend_items_spacing}")
        
        # VLAN Legend
        used_vlans = self.get_used_vlans()
        legend_items = []
        
        # VLAN names dictionary - can be expanded with more descriptive names
        vlan_names = {
            1: "Default",
            5: "Internet Uplink",
            10: "Administration",
            20: "Servere",
            30: "Netværksudstyr",
            40: "Kamera netværk",
            50: "Video Klienter",
            51: "GODIK",
            60: "Almindelige klienter",
            70: "Internet / Media",
            80: "Guest Network",
            99: "Trunk",
        }
        
        for vlan_id in sorted(used_vlans):
            color = self.vlan_colors.get(vlan_id, self.DEFAULT_VLAN_COLORS[1])
            # Get the VLAN name if it exists, otherwise use a generic name
            vlan_name = vlan_names.get(vlan_id, "")
            if vlan_name:
                legend_text = f"{vlan_id}, {vlan_name}"
            else:
                legend_text = f"{vlan_id}"
            legend_items.append((legend_text, color))
        
        # Status Legend - always show for switches with 4 or more ports
        if self.num_ports >= 4:
            # Always add all three status indicators for completeness
            legend_items.append(("Port up", "#2ecc71"))      # Green for UP
            legend_items.append(("Port down", "#e74c3c"))    # Red for DOWN
            legend_items.append(("Port disabled", "#000000"))  # Black for DISABLED
        
        # We no longer need a separate SFP port legend entry since SFP ports use their VLAN colors
        
        # Separate VLAN items and status items
        vlan_items = []
        status_items = []
        
        for label, color in legend_items:
            if label.startswith("Port "):
                status_items.append((label, color))
            else:
                vlan_items.append((label, color))
        
        # Calculate available width for legend items (switch body width minus margins)
        # Use the body_width to constrain legend items to the switch width
        available_legend_width = self.body_width - 2 * legend_x + 20  # Add 20px for margins
        
        # Calculate how much width each VLAN item would need
        vlan_item_widths = []
        for label, _ in vlan_items:
            text_width = self.get_text_width(label, font_size=10, font_family="Arial")
            # Add 15px for the color box and spacing, plus text width, plus padding
            item_width = 15 + text_width + self.legend_item_padding
            vlan_item_widths.append(item_width)
            logger.info(f"Legend item '{label}' width: {text_width}px, total: {item_width}px")
        
        # Distribute VLAN items across rows
        row_y = legend_items_y
        current_x = legend_x
        current_row_width = 0
        
        for i, ((label, color), item_width) in enumerate(zip(vlan_items, vlan_item_widths)):
            # Check if this item would exceed the available width
            if current_x + item_width > legend_x + available_legend_width and i > 0:
                # Start a new row
                row_y += self.legend_row_offset  # Move down 25px for the next row
                current_x = legend_x
                current_row_width = 0
            
            # Draw the color box
            svg.append(f'  <rect x="{current_x}" y="{row_y}" width="10" height="10" fill="{color}" stroke="#000000" stroke-width="1" />')
            
            # Draw the text
            svg.append(f'  <text x="{current_x + 15}" y="{row_y + 9}" font-family="Arial" '
                      f'font-size="10" fill="{self.theme_colors["text"]}">{label}</text>')
            
            # Move to the next item position
            current_x += item_width
            current_row_width += item_width
        
        # Add status items on a new row if there are any
        if status_items:
            # Position status section title on a new row
            status_section_y = row_y + 25
            svg.append(f'  <text x="{legend_x}" y="{status_section_y}" font-family="Arial" '
                      f'font-size="11" font-weight="bold" fill="{self.theme_colors["text"]}">Port Status:</text>')
            
            # Position status items below the status section title
            status_y = status_section_y + self.legend_items_spacing
            
            # Calculate status item widths
            status_item_widths = []
            for label, _ in status_items:
                text_width = self.get_text_width(label, font_size=10, font_family="Arial")
                item_width = 15 + text_width + self.legend_item_padding
                status_item_widths.append(item_width)
                logger.info(f"Status item '{label}' width: {text_width}px, total: {item_width}px")
            
            # Distribute status items - ensure all status items are included
            current_x = legend_x
            current_row_width = 0
            
            for i, ((label, color), item_width) in enumerate(zip(status_items, status_item_widths)):
                # Check if this item would exceed the available width
                if current_x + item_width > legend_x + available_legend_width and i > 0:
                    # Start a new row
                    status_y += 25  # Move down 25px for the next row
                    current_x = legend_x
                    current_row_width = 0
                
                # For status items, use circles instead of rectangles
                if label.startswith("Port "):
                    # Draw a circle for port status
                    circle_x = current_x + 5  # Center of the 10x10 space
                    circle_y = status_y + 5   # Center of the 10x10 space
                    svg.append(f'  <circle cx="{circle_x}" cy="{circle_y}" r="5" fill="{color}" stroke="#000000" stroke-width="1" />')
                else:
                    # Draw a rectangle for VLAN items
                    svg.append(f'  <rect x="{current_x}" y="{status_y}" width="10" height="10" fill="{color}" stroke="#000000" stroke-width="1" />')
                
                # Draw the text
                svg.append(f'  <text x="{current_x + 15}" y="{status_y + 9}" font-family="Arial" '
                          f'font-size="10" fill="{self.theme_colors["text"]}">{label}</text>')
                
                # Move to the next item position
                current_x += item_width
                current_row_width += item_width
                
                # Check if this is the last item and we need to ensure all status items are included
                if i == len(status_items) - 1:
                    # Check if we're missing the "Port disabled" status
                    if not any(item[0] == "Port disabled" for item in status_items):
                        # Add the "Port disabled" status
                        disabled_label = "Port disabled"
                        disabled_color = "#000000"  # Black for DISABLED
                        disabled_text_width = self.get_text_width(disabled_label, font_size=10, font_family="Arial")
                        disabled_item_width = 15 + disabled_text_width + self.legend_item_padding
                        
                        # Check if this item would exceed the available width
                        if current_x + disabled_item_width > legend_x + available_legend_width:
                            # Start a new row
                            status_y += 25  # Move down 25px for the next row
                            current_x = legend_x
                        
                        # Draw a circle for port disabled status
                        circle_x = current_x + 5  # Center of the 10x10 space
                        circle_y = status_y + 5   # Center of the 10x10 space
                        svg.append(f'  <circle cx="{circle_x}" cy="{circle_y}" r="5" fill="{disabled_color}" stroke="#000000" stroke-width="1" />')
                        
                        # Draw the text
                        svg.append(f'  <text x="{current_x + 15}" y="{status_y + 9}" font-family="Arial" '
                                  f'font-size="10" fill="{self.theme_colors["text"]}">{disabled_label}</text>')
                    
                    # Check if we're missing the "Port down" status
                    if not any(item[0] == "Port down" for item in status_items):
                        # Add the "Port down" status
                        down_label = "Port down"
                        down_color = "#e74c3c"  # Red for DOWN
                        down_text_width = self.get_text_width(down_label, font_size=10, font_family="Arial")
                        down_item_width = 15 + down_text_width + self.legend_item_padding
                        
                        # Check if this item would exceed the available width
                        if current_x + down_item_width > legend_x + available_legend_width:
                            # Start a new row
                            status_y += 25  # Move down 25px for the next row
                            current_x = legend_x
                        
                        # Draw a circle for port down status
                        circle_x = current_x + 5  # Center of the 10x10 space
                        circle_y = status_y + 5   # Center of the 10x10 space
                        svg.append(f'  <circle cx="{circle_x}" cy="{circle_y}" r="5" fill="{down_color}" stroke="#000000" stroke-width="1" />')
                        
                        # Draw the text
                        svg.append(f'  <text x="{current_x + 15}" y="{status_y + 9}" font-family="Arial" '
                                  f'font-size="10" fill="{self.theme_colors["text"]}">{down_label}</text>')
        
        return svg

    def generate_ports(self, adjusted_width: int, ports_per_row: int, num_rows: int) -> List[str]:
        """
        Generate the SVG content for the switch ports.
        
        Args:
            adjusted_width: The calculated width of the SVG
            ports_per_row: Number of ports per row
            num_rows: Number of rows of ports
            
        Returns:
            List of SVG lines for the ports
        """
        svg = []
        svg.append(f'  <!-- Switch ports -->')
        
        # Get port shape attributes
        port_shape_attrs = self.get_port_shape_attributes()
        
        # Define spacing constants
        start_spacing = 30  # Space from start of switch to first port
        end_spacing = 30    # Space from last SFP port to end of switch
        sfp_spacing = 20    # Space between last regular port and first SFP port (not used in SFP-only mode)
        
        # Use the original left spacing (30px)
        start_x = start_spacing
        
        # Always add model spacing even if model is empty/basic
        # This ensures consistent spacing in all switch graphics
        # Model info would be at y=60, so start at y=70 (10px below)
        start_y = 70
        
        # Track the current port number
        port_num = 1
        
        # Generate regular RJ45 ports (skip in SFP-only mode)
        if not self.sfp_only_mode:
            row_spacing = 4  # Use the same row spacing as defined in calculate_dimensions
            
            # Handle different layout modes
            if self.layout_mode == LayoutMode.SINGLE_ROW:
                # Single row layout - all ports in one row
                for i in range(self.num_ports):
                    # Make sure we generate exactly num_ports ports, regardless of port_start_number
                    if i >= self.num_ports:
                        break
                    
                    # Calculate position with port grouping if enabled
                    if self.port_group_size > 0 and i > 0:
                        # Calculate which group this port belongs to
                        group_num = i // self.port_group_size
                        
                        # Add extra spacing between groups
                        extra_spacing = group_num * self.port_group_spacing
                        
                        x = start_x + i * (self.port_width + self.port_spacing) + extra_spacing
                    else:
                        # Standard spacing without grouping
                        x = start_x + i * (self.port_width + self.port_spacing)
                    
                    # All ports are in a single row
                    y = start_y
                    
                    color = self.get_port_color(port_num)
                    
                    # Create port group with tooltip
                    # Adjust the displayed port number based on port_start_number
                    display_port_num = i + self.port_start_number
                    port_label = self.port_labels.get(port_num, str(display_port_num))
                    status = self.port_status_map.get(port_num, PortStatus.UP)
                    vlan_id = self.port_vlan_map.get(port_num, 1)
                    
                    tooltip = f"Port: {port_num}, Label: {port_label}, Status: {status.value}, VLAN: {vlan_id}"
                    
                    svg.append(f'  <g id="port-{port_num}">')
                    svg.append(f'    <title>{tooltip}</title>')
                    
                    # Port rectangle
                    svg.append(f'    <rect x="{x}" y="{y}" width="{self.port_width}" height="{self.port_height}" '
                              f'fill="{color}" stroke="#000000" stroke-width="1" '
                              f'rx="{port_shape_attrs["rx"]}" ry="{port_shape_attrs["ry"]}" />')
                    
                    # Port label - centered inside the port rectangle
                    text_x = x + (self.port_width // 2)
                    text_y = y + (self.port_height // 2) + 4  # Adjusted to center vertically
                    svg.append(f'    <text x="{text_x}" y="{text_y}" font-family="Arial" font-size="10" '
                              f'fill="white" text-anchor="middle" dominant-baseline="middle">{port_label}</text>')
                    
                    # Status indicator (small circle in corner if enabled)
                    if self.show_status_indicator:
                        indicator_x = x + self.port_width - 5
                        indicator_y = y + 5
                        # Use specific colors for each status
                        if status == PortStatus.UP:
                            indicator_color = "#2ecc71"  # Green for UP
                            stroke_color = "#000000"     # Black border
                        elif status == PortStatus.DOWN:
                            indicator_color = "#e74c3c"  # Red for DOWN
                            stroke_color = "#000000"     # Black border
                        else:  # DISABLED
                            indicator_color = "#000000"  # Black for DISABLED
                            stroke_color = "#000000"     # Black border
                        
                        svg.append(f'    <circle cx="{indicator_x}" cy="{indicator_y}" r="3" '
                                  f'fill="{indicator_color}" stroke="{stroke_color}" stroke-width="0.5" />')
                    
                    svg.append(f'  </g>')
                    
                    port_num += 1
            else:  # ZIGZAG layout
                # Calculate how many columns we need
                # For zigzag pattern, we need twice as many columns
                ports_per_row = min(self.num_ports, 48)  # Allow up to 48 ports in zigzag (24 per row)
                num_cols = (self.num_ports + 1) // 2  # Ceiling division for odd number of ports
                
                for i in range(self.num_ports):
                    # Make sure we generate exactly num_ports ports, regardless of port_start_number
                    if i >= self.num_ports:
                        break
                        
                    # Calculate row and column for zigzag pattern based on zigzag_start_position
                    if self.zigzag_start_position == "top":
                        # Even ports (0, 2, 4...) go in row 0 (top), odd ports (1, 3, 5...) go in row 1 (bottom)
                        row = i % 2
                    else:  # "bottom"
                        # Even ports (0, 2, 4...) go in row 1 (bottom), odd ports (1, 3, 5...) go in row 0 (top)
                        row = (i + 1) % 2
                    col = i // 2
                    
                    # Calculate position with port grouping if enabled
                    if self.port_group_size > 0 and col > 0:
                        # Calculate which group this port belongs to
                        # We need to use column number (not port number) for grouping
                        # since we're using a zigzag pattern
                        # For zigzag pattern, each column represents 2 ports, so we need to adjust
                        # the port_group_size to be half of the actual port_group_size
                        adjusted_group_size = max(1, self.port_group_size // 2)
                        group_num = col // adjusted_group_size
                        
                        # Add extra spacing between groups
                        extra_spacing = group_num * self.port_group_spacing
                        
                        x = start_x + col * (self.port_width + self.port_spacing) + extra_spacing
                    else:
                        # Standard spacing without grouping
                        x = start_x + col * (self.port_width + self.port_spacing)
                        
                    y = start_y + row * (self.port_height + row_spacing)
                    
                    color = self.get_port_color(port_num)
                    
                    # Create port group with tooltip
                    # Adjust the displayed port number based on port_start_number
                    display_port_num = i + self.port_start_number
                    port_label = self.port_labels.get(port_num, str(display_port_num))
                    status = self.port_status_map.get(port_num, PortStatus.UP)
                    vlan_id = self.port_vlan_map.get(port_num, 1)
                    
                    tooltip = f"Port: {port_num}, Label: {port_label}, Status: {status.value}, VLAN: {vlan_id}"
                    
                    svg.append(f'  <g id="port-{port_num}">') 
                    svg.append(f'    <title>{tooltip}</title>')
                    
                    # Port rectangle
                    svg.append(f'    <rect x="{x}" y="{y}" width="{self.port_width}" height="{self.port_height}" '
                              f'fill="{color}" stroke="#000000" stroke-width="1" '
                              f'rx="{port_shape_attrs["rx"]}" ry="{port_shape_attrs["ry"]}" />')
                    
                    # Port label - centered inside the port rectangle
                    text_x = x + (self.port_width // 2)
                    text_y = y + (self.port_height // 2) + 4  # Adjusted to center vertically
                    svg.append(f'    <text x="{text_x}" y="{text_y}" font-family="Arial" font-size="10" '
                              f'fill="white" text-anchor="middle" dominant-baseline="middle">{port_label}</text>')
                    
                    # Status indicator (small circle in corner if enabled)
                    if self.show_status_indicator:
                        indicator_x = x + self.port_width - 5
                        indicator_y = y + 5
                        # Use specific colors for each status
                        if status == PortStatus.UP:
                            indicator_color = "#2ecc71"  # Green for UP
                            stroke_color = "#000000"     # Black border
                        elif status == PortStatus.DOWN:
                            indicator_color = "#e74c3c"  # Red for DOWN
                            stroke_color = "#000000"     # Black border
                        else:  # DISABLED
                            indicator_color = "#000000"  # Black for DISABLED
                            stroke_color = "#000000"     # Black border
                        
                        svg.append(f'    <circle cx="{indicator_x}" cy="{indicator_y}" r="3" '
                                  f'fill="{indicator_color}" stroke="{stroke_color}" stroke-width="0.5" />')
                    
                    svg.append(f'  </g>')
                    
                    port_num += 1
        
        # Generate SFP ports if requested
        if self.sfp_ports > 0:
            svg.append(f'  <!-- SFP Ports -->')
            
            # SFP ports are rotated 90 degrees (wider than tall)
            sfp_height = 20
            sfp_width = 40
            sfp_port_spacing = self.port_spacing
            
            # Calculate the position of the last regular port
            # For zigzag pattern, we need to find the rightmost port
            num_cols = (self.num_ports + 1) // 2  # Ceiling division for odd number of ports
            
            # Calculate the position of the last port, considering port grouping
            if self.port_group_size > 0 and num_cols > 0:
                # Calculate how many groups we have
                num_groups = (num_cols + self.port_group_size - 1) // self.port_group_size
                
                # Calculate extra spacing from grouping
                extra_spacing = (num_groups - 1) * self.port_group_spacing if num_groups > 0 else 0
                
                last_port_x = start_x + (num_cols - 1) * (self.port_width + self.port_spacing) + extra_spacing
            else:
                last_port_x = start_x + (num_cols - 1) * (self.port_width + self.port_spacing)
            
            # Calculate the total width available for ports (adjusted_width minus margins)
            available_width = adjusted_width - 2 * 10  # 10px margin on each side
            
            # Position SFP ports based on mode
            if self.sfp_only_mode:
                # In SFP-only mode, start SFP ports at the same position as regular ports would
                sfp_start_x = start_x
            else:
                # In normal mode, position SFP ports right after the last regular port with sfp_spacing
                sfp_start_x = last_port_x + self.port_width + sfp_spacing
            
            # Handle different SFP layouts
            if self.sfp_layout == "horizontal":
                # Place all SFP ports in a single horizontal row
                
                # Calculate how many groups we have for SFP ports
                sfp_groups = 1
                if self.sfp_group_size > 0 and self.sfp_ports > 0:
                    sfp_groups = (self.sfp_ports + self.sfp_group_size - 1) // self.sfp_group_size
                
                # Calculate extra spacing from grouping
                sfp_extra_spacing = (sfp_groups - 1) * self.port_group_spacing if sfp_groups > 1 else 0
                
                # Calculate total width needed for SFP ports
                sfp_width_needed = (self.sfp_ports * sfp_width) + ((self.sfp_ports - 1) * sfp_port_spacing) + sfp_extra_spacing
                
                # Calculate the end position of the SFP ports
                sfp_end_x = sfp_start_x + sfp_width_needed
                
                # Check if this would exceed the available width
                if sfp_end_x > available_width + 10 - end_spacing:
                    logger.warning(f"SFP ports would exceed available width. Adjusting switch width.")
                
                # Position SFP ports in a single row
                for i in range(self.sfp_ports):
                    sfp_num = self.num_ports + i + self.port_start_number
                    
                    # Calculate position with SFP port grouping if enabled
                    if self.sfp_group_size > 0 and i > 0:
                        # Calculate which group this SFP port belongs to
                        group_num = i // self.sfp_group_size
                        
                        # Add extra spacing between groups
                        extra_spacing = group_num * self.port_group_spacing
                        
                        sfp_x = sfp_start_x + i * (sfp_width + sfp_port_spacing) + extra_spacing
                    else:
                        # Standard spacing without grouping
                        sfp_x = sfp_start_x + i * (sfp_width + sfp_port_spacing)
                    
                    # Position SFP ports based on layout mode
                    if self.layout_mode == LayoutMode.SINGLE_ROW:
                        # In single row layout, all SFP ports are in the same row as regular ports
                        sfp_y = start_y
                    else:
                        # In zigzag layout, SFP ports are aligned with the bottom row of regular ports
                        sfp_y = start_y + (self.port_height + 4)  # Align with bottom row
                    
                    # Use the VLAN color for the SFP port
                    sfp_color = self.get_port_color(sfp_num)
                    
                    # Create SFP port group with tooltip
                    sfp_label = self.port_labels.get(sfp_num, f"SFP{i}")
                    vlan_id = self.port_vlan_map.get(sfp_num, 1)
                    
                    tooltip = f"SFP Port: {sfp_num}, Label: {sfp_label}, VLAN: {vlan_id}"
                    
                    svg.append(f'  <g id="sfp-{i+1}">')
                    svg.append(f'    <title>{tooltip}</title>')
                    
                    # SFP port rectangle
                    svg.append(f'    <rect x="{sfp_x}" y="{sfp_y}" width="{sfp_width}" height="{sfp_height}" '
                              f'fill="{sfp_color}" stroke="#000000" stroke-width="1" rx="2" ry="2" />')
                    
                    # SFP port label
                    svg.append(f'    <text x="{sfp_x + sfp_width/2}" y="{sfp_y + sfp_height/2 + 4}" '
                              f'font-family="Arial" font-size="10" fill="white" '
                              f'text-anchor="middle" dominant-baseline="middle">{sfp_label}</text>')
                    
                    # Add status indicator for SFP ports too
                    if self.show_status_indicator:
                        # Get the status for this SFP port
                        sfp_status = self.port_status_map.get(sfp_num, PortStatus.UP)
                        indicator_x = sfp_x + sfp_width - 5
                        indicator_y = sfp_y + 5
                        
                        # Always show status indicator regardless of status
                        svg.append(f'    <circle cx="{indicator_x}" cy="{indicator_y}" r="3" '
                                  f'fill="{self.STATUS_COLORS[sfp_status]}" stroke="white" stroke-width="0.5" />')
                    
                    # Close the SFP port group
                    svg.append(f'  </g>')
                
            else:  # Default to zigzag layout
                # Place SFP ports in a zigzag pattern (similar to regular ports)
                
                # Calculate how many columns we need for SFP ports
                sfp_cols = (self.sfp_ports + 1) // 2  # Ceiling division for odd number of SFP ports
                
                # Calculate how many groups we have for SFP ports
                sfp_groups = 1
                if self.sfp_group_size > 0 and sfp_cols > 0:
                    sfp_groups = (sfp_cols + self.sfp_group_size - 1) // self.sfp_group_size
                
                # Calculate extra spacing from grouping
                sfp_extra_spacing = (sfp_groups - 1) * self.port_group_spacing if sfp_groups > 1 else 0
                
                # Calculate total width needed for SFP ports
                sfp_width_needed = (sfp_cols * sfp_width) + ((sfp_cols - 1) * sfp_port_spacing) + sfp_extra_spacing
                
                # Calculate the end position of the SFP ports
                sfp_end_x = sfp_start_x + sfp_width_needed
                
                # Check if this would exceed the available width
                if sfp_end_x > available_width + 10 - end_spacing:
                    logger.warning(f"SFP ports would exceed available width. Adjusting switch width.")
                
                # Position SFP ports in a zigzag pattern
                for i in range(self.sfp_ports):
                    sfp_num = self.num_ports + i + self.port_start_number
                    
                    # Calculate row and column for zigzag pattern based on zigzag_start_position
                    if self.zigzag_start_position == "top":
                        # Even ports (0, 2, 4...) go in row 0 (top), odd ports (1, 3, 5...) go in row 1 (bottom)
                        row = i % 2
                    else:  # "bottom"
                        # Even ports (0, 2, 4...) go in row 1 (bottom), odd ports (1, 3, 5...) go in row 0 (top)
                        row = (i + 1) % 2
                    col = i // 2
                    
                    # Calculate position with SFP port grouping if enabled
                    if self.sfp_group_size > 0 and col > 0:
                        # Calculate which group this SFP port belongs to
                        group_num = col // self.sfp_group_size
                        
                        # Add extra spacing between groups
                        extra_spacing = group_num * self.port_group_spacing
                        
                        sfp_x = sfp_start_x + col * (sfp_width + sfp_port_spacing) + extra_spacing
                    else:
                        # Standard spacing without grouping
                        sfp_x = sfp_start_x + col * (sfp_width + sfp_port_spacing)
                    
                    # Position SFP ports based on layout mode
                    if self.layout_mode == LayoutMode.SINGLE_ROW:
                        # In single row layout, all SFP ports are in the same row
                        sfp_y = start_y
                    else:
                        # In zigzag layout, position SFP ports vertically aligned with regular ports
                        sfp_y = start_y + row * (self.port_height + 4)  # 4px spacing between rows
                    
                    # Use the VLAN color for the SFP port
                    sfp_color = self.get_port_color(sfp_num)
                    
                    # Create SFP port group with tooltip
                    # Adjust the displayed SFP port number based on port_start_number
                    display_sfp_num = i + self.port_start_number
                    sfp_label = self.port_labels.get(sfp_num, f"SFP{display_sfp_num}")
                    vlan_id = self.port_vlan_map.get(sfp_num, 1)
                    
                    tooltip = f"SFP Port: {sfp_num}, Label: {sfp_label}, VLAN: {vlan_id}"
                    
                    svg.append(f'  <g id="sfp-{i+1}">')
                    svg.append(f'    <title>{tooltip}</title>')
                    
                    # SFP port rectangle
                    svg.append(f'    <rect x="{sfp_x}" y="{sfp_y}" width="{sfp_width}" height="{sfp_height}" '
                              f'fill="{sfp_color}" stroke="#000000" stroke-width="1" rx="2" ry="2" />')
                    
                    # SFP port label
                    svg.append(f'    <text x="{sfp_x + sfp_width/2}" y="{sfp_y + sfp_height/2 + 4}" '
                              f'font-family="Arial" font-size="10" fill="white" '
                              f'text-anchor="middle" dominant-baseline="middle">{sfp_label}</text>')
                    
                    # Add status indicator for SFP ports too
                    if self.show_status_indicator:
                        # Get the status for this SFP port
                        sfp_status = self.port_status_map.get(sfp_num, PortStatus.UP)
                        indicator_x = sfp_x + sfp_width - 5
                        indicator_y = sfp_y + 5
                        
                        # Always show status indicator regardless of status
                        svg.append(f'    <circle cx="{indicator_x}" cy="{indicator_y}" r="3" '
                                  f'fill="{self.STATUS_COLORS[sfp_status]}" stroke="white" stroke-width="0.5" />')
                    
                    # Close the SFP port group
                    svg.append(f'  </g>')
        return svg

    def generate_svg(self) -> str:
        """
        Generate the complete SVG content for the switch.
        
        Returns:
            SVG content as a string
        """
        # Calculate dimensions
        adjusted_width, adjusted_height, ports_per_row, num_rows = self.calculate_dimensions()
        
        # Build SVG content in sections
        svg = []
        
        # Header
        svg.extend(self.generate_svg_header(adjusted_width, adjusted_height))
        
        # Switch body
        svg.extend(self.generate_switch_body(adjusted_width, adjusted_height))
        
        # Switch details
        svg.extend(self.generate_switch_details(adjusted_width))
        
        # Status indicators
        svg.extend(self.generate_status_indicators(adjusted_width))
        
        # Ports
        svg.extend(self.generate_ports(adjusted_width, ports_per_row, num_rows))
        
        # Legend
        svg.extend(self.generate_legend(adjusted_width, adjusted_height))
        
        # Close SVG
        svg.append('</svg>')
        
        return '\n'.join(svg)

    def save_svg(self) -> None:
        """
        Generate the SVG and save it to the output file.
        
        Raises:
            IOError: If there's an error writing to the output file
        """
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
        """
        Generate the SVG, save it, and open it in the default web browser.
        
        Raises:
            IOError: If there's an error writing to the output file
        """
        self.save_svg()
        
        try:
            # Convert to absolute path
            abs_path = os.path.abspath(self.output_file)
            file_url = f"file://{abs_path}"
            
            logger.info(f"Opening SVG in browser: {file_url}")
            webbrowser.open(file_url)
        except Exception as e:
            logger.error(f"Error opening SVG in browser: {e}")
            raise
