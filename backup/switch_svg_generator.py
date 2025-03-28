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
        switch_height: int = 200,
        port_width: int = 28,
        port_height: int = 28,
        port_spacing: int = 4,
        legend_spacing: int = 15,  # Space between ports and legend
        vlan_colors: Optional[Dict[int, str]] = None,
        port_vlan_map: Optional[Dict[int, int]] = None,
        port_status_map: Optional[Dict[int, PortStatus]] = None,
        port_labels: Optional[Dict[int, str]] = None,
        output_file: str = "switch.svg",
        switch_model: SwitchModel = SwitchModel.BASIC,
        switch_name: str = "",
        theme: Theme = Theme.DARK,
        port_shape: PortShape = PortShape.ROUNDED,
        show_status_indicator: bool = True,
        sfp_ports: int = 0,  # Number of SFP ports (0-6)
        legend_position: str = "outside",  # Position of the legend: "inside" or "outside"
        switch_body_color: Optional[str] = None,  # Custom color for the switch body
        switch_body_border_color: str = "#000000",  # Border color for the switch body (default: black)
        switch_body_border_width: int = 2,  # Border width for the switch body
        port_group_size: int = 0,  # Number of ports per group (0 means no grouping)
        port_group_spacing: int = 7,  # Additional spacing between port groups in pixels
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
            sfp_ports: Number of SFP ports to add (0-6)
        """
        # Validate inputs
        if num_ports <= 0:
            raise ValueError("Number of ports must be positive")
        
        if not 0 <= sfp_ports <= 6:
            raise ValueError("Number of SFP ports must be between 0 and 6")
        
        if port_group_size < 0:
            raise ValueError("Port group size must be non-negative")
        
        self.num_ports = num_ports
        self.switch_width = max(switch_width, 400)  # Minimum width
        self.switch_height = max(switch_height, 150)  # Minimum height
        self.port_width = max(port_width, 10)  # Minimum port width
        self.port_height = max(port_height, 10)  # Minimum port height
        self.port_spacing = max(port_spacing, 2)  # Minimum spacing
        self.sfp_ports = sfp_ports
        self.port_group_size = port_group_size
        self.port_group_spacing = port_group_spacing
        
        # Use provided VLAN colors or defaults
        self.vlan_colors = vlan_colors or self.DEFAULT_VLAN_COLORS.copy()
        
        # Default port to VLAN mapping (all ports on VLAN 1 by default)
        self.port_vlan_map = port_vlan_map or {i: 1 for i in range(1, num_ports + 1)}
        
        # Default port status (all ports up by default)
        self.port_status_map = port_status_map or {i: PortStatus.UP for i in range(1, num_ports + 1)}
        
        # Port labels (empty by default)
        self.port_labels = port_labels or {}
        
        self.output_file = output_file
        self.switch_model = switch_model
        self.switch_name = switch_name or f"{num_ports}-Port Network Switch"
        self.theme = theme
        self.port_shape = port_shape
        self.show_status_indicator = show_status_indicator
        self.legend_position = legend_position.lower()  # Normalize to lowercase
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

    def get_port_color(self, port_num: int) -> str:
        """
        Get the color for a specific port based on its VLAN assignment and status.
        
        Args:
            port_num: The port number
            
        Returns:
            A color code string
        """
        # If port is disabled or down, use status color
        status = self.port_status_map.get(port_num, PortStatus.UP)
        if status != PortStatus.UP:
            return self.STATUS_COLORS[status]
        
        # Otherwise use VLAN color
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

    def calculate_dimensions(self) -> Tuple[int, int, int, int]:
        """
        Calculate the dimensions for the switch and port layout.
        
        Returns:
            Tuple of (adjusted_width, adjusted_height, ports_per_row, num_rows)
        """
        # Calculate port positioning
        ports_per_row = min(self.num_ports, 24)  # Use 24 ports per row max
        num_rows = (self.num_ports + ports_per_row - 1) // ports_per_row
        
        # Calculate space needed for ports
        row_spacing = 4  # Reduced from 6px to 4px for more compact layout
        
        # For zigzag pattern, we need half as many rows (rounded up)
        if self.num_ports > 1:
            num_rows = (self.num_ports + 1) // 2  # Ceiling division for odd number of ports
        
        ports_height = num_rows * (self.port_height + row_spacing)
        
        # Calculate space needed for header (switch name, model, etc.)
        header_height = 40  # Reduced from 50
        if self.switch_model != SwitchModel.BASIC:
            header_height += 10  # Reduced from 15
        
        # Calculate space needed for legend (at least 20px, more if many VLANs)
        legend_height = max(20, 12 * (len(self.get_used_vlans()) // 4 + 1))
        if self.sfp_ports > 0:
            # Add an entry for SFP ports in the legend
            legend_height += 20
        
        # Add extra space between ports and legend
        spacing_between_ports_and_legend = 10  # Reduced from 15
        
        # Define spacing constants
        start_spacing = 30  # Space from start of switch to first port
        end_spacing = 30    # Space from last SFP port to end of switch
        sfp_spacing = 20    # Space between last regular port and first SFP port
        
        # Calculate minimum number of ports in a row (8 normal ports and 2 SFP ports)
        min_regular_ports = 8
        min_sfp_ports = 2
        
        # Calculate how many columns we need for regular ports
        # For zigzag pattern, we need half as many columns
        regular_port_columns = (self.num_ports + 1) // 2  # Ceiling division for odd number of ports
        
        # Calculate how many columns we need for SFP ports
        sfp_columns = (self.sfp_ports + 1) // 2  # Ceiling division to get number of columns
        
        # Calculate width needed for the minimum required ports
        min_width = start_spacing + \
                   (min_regular_ports * (self.port_width + self.port_spacing)) + \
                   (sfp_spacing if min_sfp_ports > 0 else 0) + \
                   (min_sfp_ports * 40) + ((min_sfp_ports - 1) * self.port_spacing) + \
                   end_spacing
        
        # Calculate width needed for the actual number of ports
        actual_width = start_spacing + \
                      (regular_port_columns * (self.port_width + self.port_spacing)) + \
                      (sfp_spacing if self.sfp_ports > 0 else 0) + \
                      (sfp_columns * 40) + ((sfp_columns - 1) * self.port_spacing) + \
                      end_spacing
        
        # Use the larger of the minimum width, actual width, or provided switch_width
        adjusted_width = max(min_width, actual_width, self.switch_width)
        
        # Calculate height needed for SFP ports if any
        sfp_height = 0
        if self.sfp_ports > 0:
            # SFP ports are taller, so check if they need more height than regular ports
            sfp_height = self.sfp_ports * 40 + (self.sfp_ports - 1) * 10  # 40px height, 10px spacing
            ports_height = max(ports_height, sfp_height)
        
        # Use the provided switch_height for the switch body
        adjusted_height = self.switch_height
        
        # If legend is outside, add extra height for the legend below the switch
        if self.legend_position == "outside":
            # Total SVG height = switch height + spacing + legend height
            adjusted_height = self.switch_height + 20 + legend_height
        
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
        
        # If legend is outside, use the switch_height for the body height
        # Otherwise use the adjusted_height (which includes space for the legend)
        if self.legend_position == "outside":
            body_height = self.switch_height - 20  # -20 for the margins (10px top and bottom)
        else:
            body_height = adjusted_height - 20
            
        svg.append(f'  <rect x="10" y="10" width="{adjusted_width - 20}" height="{body_height}" '
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
        
        # Add model info if not basic
        if self.switch_model != SwitchModel.BASIC:
            svg.append(f'  <text x="30" y="60" font-family="Arial" font-size="12" '
                      f'fill="{self.theme_colors["text"]}">Model: {self.switch_model.value}</text>')
        
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
        
        # Power LED
        svg.append(f'  <circle cx="{adjusted_width - 60}" cy="30" r="5" fill="#2ecc71" />')
        svg.append(f'  <text x="{adjusted_width - 50}" y="35" font-family="Arial" '
                  f'font-size="12" fill="{self.theme_colors["text"]}">PWR</text>')
        
        # Status LED - increased spacing between STATUS and PWR
        svg.append(f'  <circle cx="{adjusted_width - 140}" cy="30" r="5" fill="#f1c40f" />')
        svg.append(f'  <text x="{adjusted_width - 130}" y="35" font-family="Arial" '
                  f'font-size="12" fill="{self.theme_colors["text"]}">STATUS</text>')
        
        # Add more indicators for enterprise and data center models - increased spacing
        if self.switch_model in [SwitchModel.ENTERPRISE, SwitchModel.DATA_CENTER]:
            svg.append(f'  <circle cx="{adjusted_width - 220}" cy="30" r="5" fill="#3498db" />')
            svg.append(f'  <text x="{adjusted_width - 210}" y="35" font-family="Arial" '
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
        
        # Position the legend based on the legend_position setting
        if self.legend_position == "outside":
            # Place legend under the switch
            # Start from the left side, aligned with the switch body
            legend_x = 30  # Align with the switch details
            legend_y = self.switch_height + 20  # 20px below the switch body
            
            # Add a legend title
            svg.append(f'  <text x="{legend_x}" y="{legend_y}" font-family="Arial" '
                      f'font-size="12" font-weight="bold" fill="{self.theme_colors["text"]}">Legend:</text>')
            
            # Adjust y position to start legend items below the title
            legend_y += 20
        else:
            # Default: place legend inside the switch (right side)
            # Calculate the rightmost port position
            # For zigzag pattern, we need to find the rightmost port
            ports_per_row = min(self.num_ports, 48)  # Allow up to 48 ports in zigzag (24 per row)
            num_cols = (self.num_ports + 1) // 2  # Ceiling division for odd number of ports
            
            # Calculate the position for the legend
            # Start from the right side of the switch, leaving some margin
            legend_x = adjusted_width - 200  # Position from right side
            legend_y = 70  # Start at the same y as the first row of ports
        
        # VLAN Legend
        used_vlans = self.get_used_vlans()
        legend_items = []
        
        for vlan_id in sorted(used_vlans):
            color = self.vlan_colors.get(vlan_id, self.DEFAULT_VLAN_COLORS[1])
            legend_items.append((f"VLAN {vlan_id}", color))
        
        # Status Legend (if we have non-UP ports)
        used_statuses = self.get_used_statuses()
        if len(used_statuses) > 1 or PortStatus.UP not in used_statuses:
            for status in used_statuses:
                if status != PortStatus.UP:  # Don't show UP in legend as it's the same as VLAN color
                    legend_items.append((f"Port {status.value}", self.STATUS_COLORS[status]))
        
        # Add SFP port to legend if we have any
        if self.sfp_ports > 0:
            legend_items.append(("SFP Port", "#3498db"))  # Blue
        
        # Draw legend items in a horizontal layout if outside, vertical if inside
        if self.legend_position == "outside":
            # Horizontal layout for outside legend
            for i, (label, color) in enumerate(legend_items):
                # Each legend item goes side by side
                item_x = legend_x + (i * 100)  # Space items 100px apart
                
                svg.append(f'  <rect x="{item_x}" y="{legend_y}" width="10" height="10" fill="{color}" />')
                svg.append(f'  <text x="{item_x + 15}" y="{legend_y + 9}" font-family="Arial" '
                          f'font-size="10" fill="{self.theme_colors["text"]}">{label}</text>')
        else:
            # Vertical layout for inside legend
            for i, (label, color) in enumerate(legend_items):
                # Each legend item goes on its own row
                item_y = legend_y + (i * 20)
                
                svg.append(f'  <rect x="{legend_x}" y="{item_y}" width="10" height="10" fill="{color}" />')
                svg.append(f'  <text x="{legend_x + 15}" y="{item_y + 9}" font-family="Arial" '
                          f'font-size="10" fill="{self.theme_colors["text"]}">{label}</text>')
        
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
        sfp_spacing = 20    # Space between last regular port and first SFP port
        
        # Calculate starting positions
        # Align port 1 with the start of model text (x=30)
        start_x = start_spacing
        
        # Always add model spacing even if model is empty/basic
        # This ensures consistent spacing in all switch graphics
        # Model info would be at y=60, so start at y=70 (10px below)
        start_y = 70
        
        # Generate regular RJ45 ports in a zigzag pattern
        port_num = 1
        row_spacing = 4  # Use the same row spacing as defined in calculate_dimensions
        
        # Calculate how many columns we need
        # For zigzag pattern, we need twice as many columns
        ports_per_row = min(self.num_ports, 48)  # Allow up to 48 ports in zigzag (24 per row)
        num_cols = (self.num_ports + 1) // 2  # Ceiling division for odd number of ports
        
        for i in range(self.num_ports):
            if port_num > self.num_ports:
                break
                
            # Calculate row and column for zigzag pattern
            # Even ports (1, 3, 5...) go in row 1, odd ports (2, 4, 6...) go in row 2
            row = i % 2
            col = i // 2
            
            # Calculate position with port grouping if enabled
            if self.port_group_size > 0 and col > 0:
                # Calculate which group this port belongs to
                # We need to use column number (not port number) for grouping
                # since we're using a zigzag pattern
                group_num = col // self.port_group_size
                
                # Add extra spacing between groups
                extra_spacing = group_num * self.port_group_spacing
                
                x = start_x + col * (self.port_width + self.port_spacing) + extra_spacing
            else:
                # Standard spacing without grouping
                x = start_x + col * (self.port_width + self.port_spacing)
                
            y = start_y + row * (self.port_height + row_spacing)
            
            color = self.get_port_color(port_num)
            
            # Create port group with tooltip
            port_label = self.port_labels.get(port_num, str(port_num))
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
            if self.show_status_indicator and status != PortStatus.UP:
                indicator_x = x + self.port_width - 5
                indicator_y = y + 5
                svg.append(f'    <circle cx="{indicator_x}" cy="{indicator_y}" r="3" '
                          f'fill="{self.STATUS_COLORS[status]}" stroke="white" stroke-width="0.5" />')
            
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
            
            # Position SFP ports starting sfp_spacing from the last regular port
            sfp_start_x = last_port_x + self.port_width + sfp_spacing
            sfp_start_y = start_y
            
            # Arrange SFP ports in a zigzag pattern (alternating rows)
            sfp_vertical_spacing = row_spacing  # Use the same row spacing as regular ports
            
            for i in range(self.sfp_ports):
                # Calculate row and column
                # Even ports (0, 2, 4...) go in row 1, odd ports (1, 3, 5...) go in row 2
                row = i % 2
                # Calculate column - ports are placed from left to right in each row
                col = i // 2
                
                # Calculate position
                sfp_x = sfp_start_x + col * (sfp_width + sfp_port_spacing)
                sfp_y = sfp_start_y + row * (sfp_height + sfp_vertical_spacing)
                
                # Ensure the SFP ports are within the SVG width
                if sfp_x + sfp_width > adjusted_width - end_spacing:
                    # If we're going to exceed the width, start a new row
                    sfp_x = sfp_start_x
                    sfp_y += (sfp_height + sfp_vertical_spacing) * 2  # Skip to next row pair
                
                sfp_num = self.num_ports + i + 1
                
                # SFP ports are typically for uplinks, so use a different color
                sfp_color = "#3498db"  # Blue
                
                # Create SFP port group with tooltip
                sfp_label = self.port_labels.get(sfp_num, f"SFP{i+1}")
                
                tooltip = f"SFP Port: {sfp_num}, Label: {sfp_label}"
                
                svg.append(f'  <g id="sfp-{i+1}">')
                svg.append(f'    <title>{tooltip}</title>')
                
                # SFP port rectangle - rotated 90 degrees
                svg.append(f'    <rect x="{sfp_x}" y="{sfp_y}" width="{sfp_width}" height="{sfp_height}" '
                          f'fill="{sfp_color}" stroke="#000000" stroke-width="1" rx="2" ry="2" />')
                
                # SFP port label - adjusted for rotated port
                svg.append(f'    <text x="{sfp_x + sfp_width/2}" y="{sfp_y + sfp_height/2 + 4}" '
                          f'font-family="Arial" font-size="10" fill="white" '
                          f'text-anchor="middle" dominant-baseline="middle">{sfp_label}</text>')
                
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
