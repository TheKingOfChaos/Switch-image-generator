# Single Row Switch Generator

This project provides tools to generate SVG visualizations of network switches with customizable port configurations. It includes support for creating switches with ports arranged in a single row.

## Features

- Create network switches with up to 24 normal ports in a single row
- Add SFP ports (up to 2) in a single row
- Customize port colors based on VLAN assignments
- Set port status (up/down/disabled)
- Add custom port labels
- Choose between dark and light themes
- Place legend inside or outside the switch
- Customize spacing between switch body and legend
- Customize spacing between legend title and legend items

## Files

- `switch_svg_generator.py` - The main generator class with support for both zigzag and single row layouts
- `example_layout_modes.py` - Example script demonstrating both zigzag and single row layouts

## Usage

### Creating a Single Row Switch

The recommended way to create a switch with all ports in a single row is to use the `SwitchSVGGenerator` class with the `layout_mode` parameter:

```python
from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, LayoutMode

# Create a switch with single row layout
switch = SwitchSVGGenerator(
    num_ports=24,
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Single Row Switch",
    sfp_ports=2,
    output_file="single_row_layout.svg",
    theme=Theme.DARK,
    layout_mode=LayoutMode.SINGLE_ROW  # Use single row layout
)

# Generate and save the SVG
switch.save_svg()
```

This approach provides a clean way to control the layout while using the main generator class.

### Customizing the Switch

You can customize the switch with various parameters:

```python
switch = SwitchSVGGenerator(
    num_ports=24,  # Change the number of normal ports (1-24 for single row)
    switch_width=1000,  # Adjust width to fit all ports
    switch_height=180,  # Adjust height as needed
    switch_model=SwitchModel.ENTERPRISE,  # BASIC, ENTERPRISE, DATA_CENTER, STACKABLE
    switch_name="Custom Switch Name",
    sfp_ports=2,  # Number of SFP ports (0-2 for single row)
    output_file="custom_switch.svg",
    legend_position="outside",  # "inside" or "outside"
    legend_spacing=20,  # Spacing between switch body and legend title
    legend_items_spacing=20,  # Spacing between legend title and legend items
    theme=Theme.DARK,  # DARK or LIGHT
    layout_mode=LayoutMode.SINGLE_ROW,  # Use single row layout
    # Optional: Add custom port labels
    port_labels={
        1: "WAN",
        2: "DMZ",
        25: "SFP1",
        26: "SFP2"
    },
    # Optional: Assign ports to VLANs
    port_vlan_map={
        1: 10,   # Port 1 on VLAN 10
        2: 10,   # Port 2 on VLAN 10
        3: 20,   # Port 3 on VLAN 20
    },
    # Optional: Set port statuses
    port_status_map={
        4: PortStatus.DOWN,      # Port 4 is down
        8: PortStatus.DISABLED,  # Port 8 is disabled
    }
)
```

## Examples

### Single Row Switch with 24 Ports and 2 SFP Ports

![Single Row Switch](single_row_switch.svg)

This switch has 24 normal ports and 2 SFP ports, all arranged in a single row.

## How It Works

The `layout_mode` parameter in the `SwitchSVGGenerator` class controls how ports are arranged:

- `LayoutMode.ZIGZAG` (default): Ports are arranged in a zigzag pattern (alternating top and bottom rows)
- `LayoutMode.SINGLE_ROW`: All ports are arranged in a single row

When using `LayoutMode.SINGLE_ROW`, the generator places all ports (both regular and SFP) in a single row, creating a cleaner, more straightforward representation of the switch ports.

## Example Scripts

- `examples/create_single_row_switch.py` - Creates a switch with one row of 24 ports and 2 SFP ports
- `examples/example_layout_modes.py` - Demonstrates both zigzag and single row layouts
- `examples/example_custom_single_row_switch.py` - Creates a customized single row switch with VLAN colors and port statuses
