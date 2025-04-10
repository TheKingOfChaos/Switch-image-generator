# Network Switch SVG Generator

A Python package for generating SVG visualizations of network switches with configurable layouts and port configurations.

## Installation

```bash
pip install switch_svg_generator
```

## Features

- Generate network switch SVG visualizations with different layouts:
  - Single row layout with up to 24 normal ports and 2 SFP ports
  - Double row (zigzag) layout with up to 48 normal ports and 6 SFP ports
  - SFP-only mode with 4-32 SFP ports and no regular ports
- Flexible SFP port layout options:
  - Zigzag layout (default) - SFP ports in a zigzag pattern (similar to regular ports)
  - Horizontal layout - All SFP ports in a single horizontal row
- Group ports with additional spacing between groups (both regular and SFP ports)
- Customize port colors based on VLAN assignments
- Set port status (up/down/disabled)
- Add custom port labels
- Choose between dark and light themes
- Place legend inside or outside the switch

## Usage

### Command-Line Interface

```bash
# Generate a single row switch with 24 normal ports and 2 SFP ports
switch-svg-generator --layout single --ports 24 --sfp 2

# Generate a double row switch with 48 normal ports and 6 SFP ports
switch-svg-generator --layout double --ports 48 --sfp 6

# Generate an SFP-only switch with 8 SFP ports
switch-svg-generator --layout sfp-only --sfp 8

# Use interactive mode for guided configuration
switch-svg-generator --interactive
```

### Command-Line Options

| Option                           | Description                                                                           |
|----------------------------------|---------------------------------------------------------------------------------------|
| `--layout {single,double,sfp-only}` | Layout type: single for one row, double for two rows (zigzag), sfp-only for SFP ports only |
| `--ports N`                      | Number of normal ports (1-24 for single, 1-48 for double, 0 for sfp-only)            |
| `--sfp N`                        | Number of SFP ports (0-2 for single, 0-6 for double, 4-32 for sfp-only)              |
| `--output FILENAME`              | Output SVG filename                                                                   |
| `--name NAME`                    | Custom switch name                                                                    |
| `--theme {dark,light}`           | Color theme (default: dark)                                                           |
| `--interactive`                  | Run in interactive mode (prompts for input)                                           |

### Python API

```python
from switch_svg_generator import SwitchSVGGenerator, PortStatus, SwitchModel, Theme, PortShape
from switch_svg_generator import SingleRowSwitchGenerator

# Example 1: Basic 24-port switch with default settings
basic_switch = SwitchSVGGenerator(
    num_ports=24,
    output_file="basic_switch.svg"
)
basic_switch.save_svg()

# Example 2: Enterprise switch with custom VLAN assignments and port statuses
# Define VLAN assignments
port_vlan_map = {
    1: 10,   # Port 1 on VLAN 10
    2: 10,   # Port 2 on VLAN 10
    3: 20,   # Port 3 on VLAN 20
    4: 20,   # Port 4 on VLAN 20
}

# Define port statuses
port_status_map = {
    4: PortStatus.DOWN,      # Port 4 is down
    8: PortStatus.DISABLED,  # Port 8 is disabled
}

# Define custom port labels
port_labels = {
    1: "WAN",
    2: "DMZ",
    3: "SRV1",
    4: "SRV2",
}

enterprise_switch = SwitchSVGGenerator(
    num_ports=48,
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Core Switch 1",
    port_vlan_map=port_vlan_map,
    port_status_map=port_status_map,
    port_labels=port_labels,
    output_file="enterprise_switch.svg"
)
enterprise_switch.save_svg()

# Example 3: Single row switch with SFP ports
single_row_switch = SingleRowSwitchGenerator(
    num_ports=24,
    sfp_ports=2,
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Access Switch",
    output_file="single_row_switch.svg"
)
single_row_switch.save_svg()
```

## License

This project is licensed under the GNU General Public License v3 (GPLv3).
