"""
Network Switch SVG Generator - Dimensions Module
----------------------------
This module contains the dimension calculation methods for the switch SVG generator.
"""

from typing import Tuple
from .core_base import SwitchModel


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
        # Normal mode - calculate regular port layout
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
