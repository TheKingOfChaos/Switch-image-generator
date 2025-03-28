# Single Row Switch Generator

This project provides tools to generate SVG visualizations of network switches with customizable port configurations. It includes a specialized generator for creating switches with ports arranged in a single row.

## Features

- Create network switches with up to 24 normal ports in a single row
- Add SFP ports (up to 6) in a single row
- Customize port colors based on VLAN assignments
- Set port status (up/down/disabled)
- Add custom port labels
- Choose between dark and light themes
- Place legend inside or outside the switch
- Customize spacing between switch body and legend
- Customize spacing between legend title and legend items

## Files

- `switch_svg_generator.py` - The base generator class (original implementation)
- `single_row_switch_generator.py` - Extended generator that places all ports in a single row
- `create_single_row_switch.py` - Script to create a switch with one row of 24 ports and 2 SFP ports
- `one_row_switch_with_sfp.py` - Alternative implementation using the original generator (creates a zigzag pattern)

## Usage

### Creating a Single Row Switch

To create a switch with all ports in a single row:

```bash
python3 create_single_row_switch.py
```

This will generate `single_row_switch.svg` with 24 normal ports and 2 SFP ports in a single row.

### Customizing the Switch

You can modify `create_single_row_switch.py` to customize the switch:

```python
switch = SingleRowSwitchGenerator(
    num_ports=24,  # Change the number of normal ports (1-48)
    switch_width=1000,  # Adjust width to fit all ports
    switch_height=180,  # Adjust height as needed
    switch_model=SwitchModel.ENTERPRISE,  # BASIC, ENTERPRISE, DATA_CENTER, STACKABLE
    switch_name="Custom Switch Name",
    sfp_ports=2,  # Number of SFP ports (0-6)
    output_file="custom_switch.svg",
    legend_position="outside",  # "inside" or "outside"
    legend_spacing=20,  # Spacing between switch body and legend title
    legend_items_spacing=20,  # Spacing between legend title and legend items
    theme=Theme.DARK,  # DARK or LIGHT
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

The `SingleRowSwitchGenerator` extends the base `SwitchSVGGenerator` class and overrides the `generate_ports` method to place all ports in a single row instead of the default zigzag pattern. This allows for a cleaner, more straightforward representation of the switch ports.
