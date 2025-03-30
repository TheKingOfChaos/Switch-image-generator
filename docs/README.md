# Network Switch SVG Generator

A Python tool for generating SVG diagrams of network switches with configurable ports, VLAN assignments, and port statuses.

## Features

- Generate SVG representations of network switches
- Configure number of ports (supports any number of ports)
- VLAN-based port coloring
- Port status indicators (up/down/disabled)
- Support for different switch models (basic, enterprise, data center, stackable)
- Customizable port labels
- Dark/light theme support
- Different port shapes (square, rounded, circular)
- Preview generated SVGs in a web browser
- Comprehensive command-line interface

## Installation

No installation required. Simply download the `switch_svg_generator.py` script and run it with Python 3.

```bash
# Make the script executable (Linux/macOS)
chmod +x switch_svg_generator.py
```

## Usage

### Command Line Interface

```bash
# Basic usage - generate a 24-port switch SVG
./switch_svg_generator.py

# Specify number of ports and output file
./switch_svg_generator.py --ports 48 --output my_switch.svg

# Assign ports to VLANs
./switch_svg_generator.py --port-vlan "1:10" "2:10" "3:20" "4:20"

# Set port statuses
./switch_svg_generator.py --port-status "1:up" "2:down" "3:disabled"

# Add custom port labels
./switch_svg_generator.py --port-label "1:WAN" "2:DMZ" "3:SRV1"

# Customize VLAN colors
./switch_svg_generator.py --vlan-color "1:#3498db" "10:#2ecc71" "20:#e74c3c"

# Change switch model
./switch_svg_generator.py --model enterprise

# Use light theme
./switch_svg_generator.py --theme light

# Change port shape
./switch_svg_generator.py --port-shape circular

# Place legend outside the switch
./switch_svg_generator.py --legend-position outside

# Preview in browser
./switch_svg_generator.py --preview

# Enable verbose logging
./switch_svg_generator.py --verbose
```

### Python API

You can also use the `SwitchSVGGenerator` class directly in your Python code:

```python
from switch_svg_generator import SwitchSVGGenerator, PortStatus, SwitchModel, Theme, PortShape

# Create a basic switch
generator = SwitchSVGGenerator(
    num_ports=24,
    output_file="switch.svg"
)
generator.save_svg()

# Create a more complex switch
generator = SwitchSVGGenerator(
    num_ports=48,
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Core Switch",
    port_vlan_map={1: 10, 2: 10, 3: 20},
    port_status_map={4: PortStatus.DOWN, 8: PortStatus.DISABLED},
    port_labels={1: "WAN", 2: "DMZ"},
    theme=Theme.LIGHT,
    port_shape=PortShape.CIRCULAR,
    legend_position="outside",  # Place legend under and outside the switch
    legend_spacing=20,  # Spacing between switch body and legend title
    legend_items_spacing=20,  # Spacing between legend title and legend items
    switch_body_color="#4a86e8",  # Custom blue color for the switch body
    switch_body_border_color="#000000",  # Black border
    switch_body_border_width=2,  # 2px border width
    output_file="enterprise_switch.svg"
)
generator.save_svg()

# Preview in browser
generator.preview_svg()
```

See `example_usage.py` for more detailed examples.

## Command Line Options

| Option                        | Description                                                          |
|-------------------------------|----------------------------------------------------------------------|
| `--ports`                     | Number of ports (default: 24)                                        |
| `--output`                    | Output file path (default: switch.svg)                               |
| `--name`                      | Custom name for the switch                                           |
| `--port-vlan`                 | Port-VLAN mappings in format "port:vlan" (e.g., "1:10" "2:20")       |
| `--port-status`               | Port-Status mappings in format "port:status" (e.g., "1:up" "2:down") |
| `--port-label`                | Port-Label mappings in format "port:label" (e.g., "1:WAN" "2:LAN1")  |
| `--vlan-color`                | VLAN-Color mappings in format "vlan:#RRGGBB" (e.g., "10:#FF0000")    |
| `--model`                     | Switch model type: basic, enterprise, data_center, stackable         |
| `--theme`                     | Color theme: dark, light                                             |
| `--port-shape`                | Port shape: square, rounded, circular                                |
| `--legend-position`           | Legend position: inside, outside                                     |
| `--legend-spacing`            | Spacing between switch body and legend title in pixels               |
| `--legend-items-spacing`      | Spacing between legend title and legend items in pixels              |
| `--switch-body-color`         | Custom color for the switch body (e.g., "#4a86e8")                   |
| `--switch-body-border-color`  | Border color for the switch body (default: black)                    |
| `--switch-body-border-width`  | Border width for the switch body in pixels (default: 2)              |
| `--hide-status-indicator`     | Hide port status indicators                                          |
| `--preview`                   | Open the generated SVG in a web browser                              |
| `--verbose`                   | Enable verbose logging                                               |

## Examples

### Basic 24-port switch
```bash
./switch_svg_generator.py
```

### Enterprise switch with custom VLAN assignments
```bash
./switch_svg_generator.py --model enterprise --name "Core Switch" \
  --port-vlan "1:10" "2:10" "3:20" "4:20" "5:30" "6:30" \
  --port-status "4:down" "8:disabled" \
  --port-label "1:WAN" "2:DMZ" "3:SRV1" "4:SRV2" \
  --output enterprise_switch.svg
```

### Data center switch with light theme and circular ports
```bash
./switch_svg_generator.py --model data_center --name "Data Center Switch" \
  --ports 48 --theme light --port-shape circular \
  --output data_center_switch.svg
```

### Switch with custom body color and border
```bash
./switch_svg_generator.py --model enterprise --name "Custom Colored Switch" \
  --switch-body-color "#4a86e8" --switch-body-border-color "#000000" --switch-body-border-width 2 \
  --legend-position outside \
  --output custom_switch_colors.svg
```

### Switch with custom legend spacing
```bash
./switch_svg_generator.py --model enterprise --name "Switch with Custom Legend Spacing" \
  --legend-spacing 40 --legend-items-spacing 30 \
  --output custom_legend_spacing.svg
```

## License

This project is open source and available under the MIT License.
