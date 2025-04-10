"""
Network Switch SVG Generator - Legend Module
----------------------------
This module contains the legend generation methods for the switch SVG generator.
"""

from typing import List
from .core_base import PortStatus


def generate_legend(self, adjusted_width: int, adjusted_height: int) -> List[str]:
    """
    Generate the SVG content for the legend.
    
    Args:
        adjusted_width: The calculated width of the SVG
        adjusted_height: The calculated height of the SVG
        
    Returns:
        List of SVG lines for the legend
    """
    svg = []
    svg.append(f'  <!-- Legend -->')
    
    # Get the set of VLANs that are actually used
    used_vlans = self.get_used_vlans()
    
    # Get the set of statuses that are actually used
    used_statuses = self.get_used_statuses()
    
    # Skip legend if no VLANs or statuses are used
    if not used_vlans and not used_statuses:
        return svg
    
    # Calculate legend position
    # Position the legend below the switch body
    legend_y = self.switch_height + self.legend_spacing
    
    # Add legend title
    svg.append(f'  <text x="30" y="{legend_y}" font-family="Arial" font-size="12" '
              f'font-weight="bold" fill="{self.theme_colors["text"]}">Legend:</text>')
    
    # Position VLAN section title below the legend title with additional 3px spacing
    vlan_section_y = legend_y + self.legend_items_spacing + 3  # Added 3px extra spacing
    svg.append(f'  <text x="30" y="{vlan_section_y}" font-family="Arial" '
              f'font-size="11" font-weight="bold" fill="{self.theme_colors["text"]}">VLANs:</text>')
    
    # Position legend items below the VLAN section title
    legend_items_y = vlan_section_y + self.legend_items_spacing
    
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
    
    # Calculate available width for legend items
    available_legend_width = adjusted_width - 2 * 30  # 30px margin on each side
    
    # VLAN Legend
    vlan_items = []
    for vlan_id in sorted(self.get_used_vlans()):
        color = self.vlan_colors.get(vlan_id, self.DEFAULT_VLAN_COLORS[1])
        # Get the VLAN name if it exists, otherwise use a generic name
        vlan_name = vlan_names.get(vlan_id, "")
        if vlan_name:
            label = f"{vlan_id}, {vlan_name}"
        else:
            label = f"{vlan_id}"
        vlan_items.append((label, color))
    
    # Calculate how much width each VLAN item would need
    vlan_item_widths = []
    for label, _ in vlan_items:
        text_width = self.get_text_width(label, font_size=10, font_family="Arial")
        # Add 15px for the color box and spacing, plus text width, plus padding
        item_width = 15 + text_width + self.legend_item_padding
        vlan_item_widths.append(item_width)
    
    # Distribute VLAN items across rows
    row_y = legend_items_y
    current_x = 30
    
    for i, ((label, color), item_width) in enumerate(zip(vlan_items, vlan_item_widths)):
        # Check if this item would exceed the available width
        if current_x + item_width > 30 + available_legend_width and i > 0:
            # Start a new row
            row_y += 25  # Move down 25px for the next row
            current_x = 30
        
        # Draw the color box
        svg.append(f'  <rect x="{current_x}" y="{row_y}" width="10" height="10" fill="{color}" stroke="#000000" stroke-width="1" />')
        
        # Draw the text
        svg.append(f'  <text x="{current_x + 15}" y="{row_y + 9}" font-family="Arial" '
                  f'font-size="10" fill="{self.theme_colors["text"]}">{label}</text>')
        
        # Move to the next item position
        current_x += item_width
    
    # Add status items on a new row
    # Position status section title on a new row
    status_section_y = row_y + 25
    svg.append(f'  <text x="30" y="{status_section_y}" font-family="Arial" '
              f'font-size="11" font-weight="bold" fill="{self.theme_colors["text"]}">Port Status:</text>')
    
    # Position status items below the status section title
    status_y = status_section_y + self.legend_items_spacing
    
    # Status items
    status_items = []
    for status in self.get_used_statuses():
        if status == PortStatus.UP:
            label = "Port up"
            color = "#2ecc71"  # Green
        elif status == PortStatus.DOWN:
            label = "Port down"
            color = "#e74c3c"  # Red
        else:  # DISABLED
            label = "Port disabled"
            color = "#000000"  # Black
        status_items.append((label, color))
    
    # Calculate status item widths
    status_item_widths = []
    for label, _ in status_items:
        text_width = self.get_text_width(label, font_size=10, font_family="Arial")
        item_width = 15 + text_width + self.legend_item_padding
        status_item_widths.append(item_width)
    
    # Distribute status items
    current_x = 30
    
    for i, ((label, color), item_width) in enumerate(zip(status_items, status_item_widths)):
        # Check if this item would exceed the available width
        if current_x + item_width > 30 + available_legend_width and i > 0:
            # Start a new row
            status_y += 25  # Move down 25px for the next row
            current_x = 30
        
        # Draw a circle for port status
        circle_x = current_x + 5  # Center of the 10x10 space
        circle_y = status_y + 5   # Center of the 10x10 space
        svg.append(f'  <circle cx="{circle_x}" cy="{circle_y}" r="5" fill="{color}" stroke="#000000" stroke-width="1" />')
        
        # Draw the text
        svg.append(f'  <text x="{current_x + 15}" y="{status_y + 9}" font-family="Arial" '
                  f'font-size="10" fill="{self.theme_colors["text"]}">{label}</text>')
        
        # Move to the next item position
        current_x += item_width
    
    return svg
