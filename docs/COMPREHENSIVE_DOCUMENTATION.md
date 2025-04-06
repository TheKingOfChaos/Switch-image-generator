# Network Switch SVG Generator - Comprehensive Documentation

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
- [Generator Types](#generator-types)
  - [Standard Switch Generator](#standard-switch-generator)
  - [Single Row Switch Generator](#single-row-switch-generator)
  - [Configurable Switch Generator](#configurable-switch-generator)
  - [SFP-Only Mode](#sfp-only-mode)
- [Layout Options](#layout-options)
  - [Single Row Layout](#single-row-layout)
  - [Double Row (Zigzag) Layout](#double-row-zigzag-layout)
  - [SFP-Only Layout](#sfp-only-layout)
  - [SFP Port Layout Options](#sfp-port-layout-options)
- [Complete Configuration Reference](#complete-configuration-reference)
  - [Basic Configuration](#basic-configuration)
  - [Switch Appearance](#switch-appearance)
  - [Port Configuration](#port-configuration)
  - [VLAN and Status Settings](#vlan-and-status-settings)
  - [Legend Configuration](#legend-configuration)
  - [SFP Port Configuration](#sfp-port-configuration)
- [Command-Line Interface](#command-line-interface)
  - [Basic CLI Options](#basic-cli-options)
  - [Advanced CLI Options](#advanced-cli-options)
  - [Interactive Mode](#interactive-mode)
  - [CLI Examples](#cli-examples)
- [Python API Reference](#python-api-reference)
  - [SwitchSVGGenerator Class](#switchsvggenerator-class)
  - [SingleRowSwitchGenerator Class](#singlerowswitchgenerator-class)
  - [API Examples](#api-examples)
- [Advanced Customization](#advanced-customization)
  - [Custom Port Colors](#custom-port-colors)
  - [Custom Switch Body Styling](#custom-switch-body-styling)
  - [Port Grouping](#port-grouping)
  - [Custom Model Names](#custom-model-names)
- [Examples Gallery](#examples-gallery)

## Overview

The Network Switch SVG Generator is a tool for creating SVG visualizations of network switches with configurable layouts and port configurations. It allows you to generate visual representations of network switches with customizable ports, VLAN assignments, port statuses, and more.

### Key Features

- Generate network switch SVG visualizations with different layouts:
  - Single row layout with up to 24 normal ports and 2 SFP ports
  - Double row (zigzag) layout with up to 48 normal ports and 6 SFP ports
  - SFP-only mode with 4-32 SFP ports and no regular ports
- Flexible SFP port layout options:
  - Zigzag layout (default) - SFP ports in a zigzag pattern
  - Horizontal layout - All SFP ports in a single horizontal row
- Group ports with additional spacing between groups (both regular and SFP ports)
- Customize port colors based on VLAN assignments
- Set port status (up/down/disabled)
- Add custom port labels
- Choose between dark and light themes
- Place legend inside or outside the switch
- Customize spacing between switch body and legend
- Customize spacing between legend title and legend items
- Different port shapes (square, rounded, circular)
- Custom switch body colors and borders

## Project Structure

```
switch_grafic_generator/
├── src/                  # Source code
│   ├── switch_svg_generator.py         # Base generator class
│   ├── single_row_switch_generator.py  # Single row layout generator
│   ├── configurable_switch_generator.py # Configurable generator with CLI
│   └── generate_switch.py              # Internal entry point
├── examples/             # Example scripts
│   ├── create_single_row_switch.py     # Example of single row switch
│   ├── create_sfp_only_switch.py       # Example of SFP-only switch
│   ├── create_one_row_switch_with_sfp.py # Example with SFP ports
│   └── ...                             # Other examples
├── docs/                 # Documentation
│   ├── README.md                       # Original README
│   ├── CONFIGURABLE_SWITCH_README.md   # Configurable switch documentation
│   └── SINGLE_ROW_SWITCH_README.md     # Single row switch documentation
├── output/               # Generated SVG files
│   └── ...                             # SVG output files
├── tests/                # Test scripts
│   └── ...                             # Test files
├── tools/                # Utility scripts
│   └── ...                             # Tool files
└── generate_switch.py    # Main script (entry point)
```

## Getting Started

### Installation

No installation is required. Simply download the project files and run the scripts with Python 3.

```bash
# Make the main script executable (Linux/macOS)
chmod +x generate_switch.py
```

### Quick Start

#### Using the Command-Line Interface

```bash
# Generate a single row switch with 24 normal ports and 2 SFP ports
./generate_switch.py --layout single --ports 24 --sfp 2

# Generate a double row switch with 48 normal ports and 6 SFP ports
./generate_switch.py --layout double --ports 48 --sfp 6

# Generate an SFP-only switch with 8 SFP ports
./generate_switch.py --layout sfp-only --sfp 8

# Use interactive mode for guided configuration
./generate_switch.py --interactive
```

#### Using the Python API

```python
from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus

# Create a basic switch
generator = SwitchSVGGenerator(
    num_ports=24,
    output_file="switch.svg"
)
generator.save_svg()

# Preview in browser
generator.preview_svg()
```

## Generator Types

The project provides three main generator types, each with its own specific use case.

### Standard Switch Generator

The `SwitchSVGGenerator` class is the base generator that creates switches with ports arranged in a zigzag pattern (two rows). It supports up to 48 normal ports and 6 SFP ports.

```python
from src.switch_svg_generator import SwitchSVGGenerator

generator = SwitchSVGGenerator(
    num_ports=48,
    sfp_ports=6,
    output_file="standard_switch.svg"
)
generator.save_svg()
```

### Single Row Switch Generator

The `SingleRowSwitchGenerator` class extends the base generator to create switches with all ports arranged in a single row. It supports up to 24 normal ports and 2 SFP ports.

```python
from src.single_row_switch_generator import SingleRowSwitchGenerator

generator = SingleRowSwitchGenerator(
    num_ports=24,
    sfp_ports=2,
    output_file="single_row_switch.svg"
)
generator.save_svg()
```

### Configurable Switch Generator

The configurable switch generator provides a command-line interface for generating switches with different layouts. It's accessible through the `generate_switch.py` script.

```bash
./generate_switch.py --layout single --ports 24 --sfp 2
```

### SFP-Only Mode

SFP-only mode creates a switch with only SFP ports (no regular RJ45 ports). It supports 4-32 SFP ports.

```python
from src.switch_svg_generator import SwitchSVGGenerator

generator = SwitchSVGGenerator(
    sfp_ports=8,
    sfp_only_mode=True,
    output_file="sfp_only_switch.svg"
)
generator.save_svg()
```

## Layout Options

### Single Row Layout

The single row layout places all ports in a single horizontal row. It's suitable for switches with up to 24 normal ports and 2 SFP ports.

- Uses `SingleRowSwitchGenerator` class
- Maximum 24 normal ports
- Maximum 2 SFP ports
- All ports are arranged in a single row

### Double Row (Zigzag) Layout

The double row layout places ports in a zigzag pattern (alternating between two rows). It's suitable for switches with up to 48 normal ports and 6 SFP ports.

- Uses `SwitchSVGGenerator` class
- Maximum 48 normal ports
- Maximum 6 SFP ports
- Ports are arranged in a zigzag pattern

### SFP-Only Layout

The SFP-only layout creates a switch with only SFP ports (no regular RJ45 ports). It's suitable for switches with 4-32 SFP ports.

- Uses `SwitchSVGGenerator` class with `sfp_only_mode=True`
- No regular ports
- 4-32 SFP ports
- SFP ports can be arranged in different layouts

### SFP Port Layout Options

SFP ports can be arranged in different layouts:

- **Zigzag Layout (Default)**: SFP ports are arranged in a zigzag pattern (alternating between two rows)
- **Horizontal Layout**: All SFP ports are arranged in a single horizontal row

```python
# Zigzag layout (default)
generator = SwitchSVGGenerator(
    sfp_ports=8,
    sfp_layout="zigzag",
    output_file="sfp_zigzag.svg"
)

# Horizontal layout
generator = SwitchSVGGenerator(
    sfp_ports=8,
    sfp_layout="horizontal",
    output_file="sfp_horizontal.svg"
)
```

## Complete Configuration Reference

### Basic Configuration

| Parameter       | Type | Default      | Description |
|-----------------|------|--------------|-----------------------------------------------------------------|
| `num_ports`     | int  | 24           | Number of normal ports (5-48)                                   |
| `sfp_ports`     | int  | 0            | Number of SFP ports (0-6 in normal mode, 4-32 in SFP-only mode) |
| `output_file`   | str  | "switch.svg" | Path to save the SVG file                                       |
| `switch_width`  | int  | 800          | Width of the switch in pixels                                   |
| `switch_height` | int  | 130          | Height of the switch in pixels                                  |

### Switch Appearance

| Parameter                  | Type        | Default           | Description                                                      |
|----------------------------|-------------|-------------------|------------------------------------------------------------------|
| `switch_model`             | SwitchModel | SwitchModel.BASIC | Model of the switch (BASIC, ENTERPRISE, DATA_CENTER, STACKABLE)  |
| `model_name`               | str         | ""                | Custom model name to display on the switch                       |
| `switch_name`              | str         | ""                | Custom name for the switch                                       |
| `theme`                    | Theme       | Theme.LIGHT       | Color theme (DARK, LIGHT)                                        |
| `switch_body_color`        | str         | None              | Custom color for the switch body (e.g., "#4a86e8")               |
| `switch_body_border_color` | str         | "#000000"         | Border color for the switch body                                 |
| `switch_body_border_width` | int         | 2                 | Border width for the switch body in pixels                       |

### Port Configuration

| Parameter               | Type      | Default          | Description                                           |
|-------------------------|-----------|------------------|-------------------------------------------------------|
| `port_width`            | int       | 28               | Width of each port in pixels                          |
| `port_height`           | int       | 28               | Height of each port in pixels                         |
| `port_spacing`          | int       | 4                | Spacing between ports in pixels                       |
| `port_shape`            | PortShape | PortShape.SQUARE | Shape of the ports (SQUARE, ROUNDED, CIRCULAR)        |
| `port_group_size`       | int       | 0                | Number of ports per group (0 means no grouping)       |
| `port_group_spacing`    | int       | 7                | Additional spacing between port groups in pixels      |
| `show_status_indicator` | bool      | True             | Whether to show port status indicators                |
| `port_start_number`     | int       | 1                | Starting port number (0 or 1)                         |
| `zigzag_start_position` | str       | "top"            | First port position in zigzag pattern ("top" or "bottom") |


#### Port Numbering Options

The `port_start_number` parameter allows you to choose whether port numbering starts from 0 or 1:

- `port_start_number=1` (default): Port numbering starts from 1 (1, 2, 3, ...) and SFP ports from SFP1
- `port_start_number=0`: Port numbering starts from 0 (0, 1, 2, ...) and SFP ports from SFP0

This affects the port labels displayed on the switch and is useful for different network equipment conventions.

#### Zigzag Pattern Options

The `zigzag_start_position` parameter controls whether the first port in a zigzag pattern is on the top or bottom row:

- `zigzag_start_position="top"` (default): First port is on the top row, second port is on the bottom row, and so on
- `zigzag_start_position="bottom"`: First port is on the bottom row, second port is on the top row, and so on

This allows you to match the port layout of different switch models.

#### Combining Port Numbering and Zigzag Options

You can combine these options to create four different port configurations:

1. Default: `port_start_number=1, zigzag_start_position="top"`
   - Port numbering starts from 1
   - First port (1) is on the top row
   - Second port (2) is on the bottom row

2. Start from 0: `port_start_number=0, zigzag_start_position="top"`
   - Port numbering starts from 0
   - First port (0) is on the top row
   - Second port (1) is on the bottom row

3. First port on bottom: `port_start_number=1, zigzag_start_position="bottom"`
   - Port numbering starts from 1
   - First port (1) is on the bottom row
   - Second port (2) is on the top row

4. Start from 0, first port on bottom: `port_start_number=0, zigzag_start_position="bottom"`
   - Port numbering starts from 0
   - First port (0) is on the bottom row
   - Second port (1) is on the top row

### VLAN and Status Settings

| Parameter         | Type                  | Default                                           | Description                                      |
|-------------------|-----------------------|---------------------------------------------------|--------------------------------------------------|
| `vlan_colors`     | Dict[int, str]        | DEFAULT_VLAN_COLORS                               | Dictionary mapping VLAN IDs to color codes       |
| `port_vlan_map`   | Dict[int, int]        | {i: 1 for i in range(1, num_ports+1)}             | Dictionary mapping port numbers to VLAN IDs      |
| `port_status_map` | Dict[int, PortStatus] | {i: PortStatus.UP for i in range(1, num_ports+1)} | Dictionary mapping port numbers to their status  |
| `port_labels`     | Dict[int, str]        | {}                                                | Dictionary mapping port numbers to custom labels |

### Legend Configuration

| Parameter              | Type | Default | Description                                              |
|------------------------|------|---------|----------------------------------------------------------|
| `legend_spacing`       | int  | 20      | Spacing between switch body and legend title in pixels   |
| `legend_items_spacing` | int  | 8       | Spacing between legend title and legend items in pixels  |
| `legend_item_padding`  | int  | 3       | Padding between legend items (horizontal spacing)        |

### SFP Port Configuration

| Parameter        | Type | Default   | Description                                           |
|------------------|------|-----------|-------------------------------------------------------|
| `sfp_only_mode`  | bool | False     | When True, creates a switch with only SFP ports       |
| `sfp_layout`     | str  | "zigzag"  | Layout of SFP ports ("zigzag" or "horizontal")        |
| `sfp_group_size` | int  | 0         | Number of SFP ports per group (0 means no grouping)   |

## Command-Line Interface

The command-line interface is provided by the `generate_switch.py` script, which uses the configurable switch generator.

### Basic CLI Options

| Option                              | Description                                                                                |
|-------------------------------------|--------------------------------------------------------------------------------------------|
| `--layout {single,double,sfp-only}` | Layout type: single for one row, double for two rows (zigzag), sfp-only for SFP ports only |
| `--ports N`                         | Number of normal ports (1-24 for single, 1-48 for double, 0 for sfp-only)                  |
| `--sfp N`                           | Number of SFP ports (0-2 for single, 0-6 for double, 4-32 for sfp-only)                    |
| `--output FILENAME`                 | Output SVG filename                                                                        |
| `--name NAME`                       | Custom switch name                                                                         |
| `--theme {dark,light}`              | Color theme (default: dark)                                                                |
| `--interactive`                     | Run in interactive mode (prompts for input)                                                |

### Advanced CLI Options

These options are available when using the base `switch_svg_generator.py` script directly:

| Option                        | Description                                                          |
|-------------------------------|----------------------------------------------------------------------|
| `--port-vlan`                 | Port-VLAN mappings in format "port:vlan" (e.g., "1:10" "2:20")       |
| `--port-status`               | Port-Status mappings in format "port:status" (e.g., "1:up" "2:down") |
| `--port-label`                | Port-Label mappings in format "port:label" (e.g., "1:WAN" "2:LAN1")  |
| `--vlan-color`                | VLAN-Color mappings in format "vlan:#RRGGBB" (e.g., "10:#FF0000")    |
| `--model`                     | Switch model type: basic, enterprise, data_center, stackable         |
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

### Interactive Mode

The interactive mode provides a guided experience for generating switch SVGs. It prompts for:

1. Layout type (single row, double row, or SFP-only)
2. Number of normal ports
3. Number of SFP ports
4. Output filename
5. Theme (dark or light)

```bash
./generate_switch.py --interactive
```

### CLI Examples

```bash
# Generate a single row switch with 24 normal ports and 2 SFP ports
./generate_switch.py --layout single --ports 24 --sfp 2

# Generate a double row switch with 48 normal ports and 6 SFP ports
./generate_switch.py --layout double --ports 48 --sfp 6

# Generate an SFP-only switch with 8 SFP ports
./generate_switch.py --layout sfp-only --sfp 8

# Specify a custom output filename
./generate_switch.py --layout single --ports 16 --sfp 2 --output my_switch.svg

# Use light theme
./generate_switch.py --layout double --ports 24 --sfp 4 --theme light

# Provide a custom switch name
./generate_switch.py --layout single --ports 24 --sfp 2 --name "My Custom Switch"
```

## Python API Reference

### SwitchSVGGenerator Class

The `SwitchSVGGenerator` class is the base generator class that creates switches with ports arranged in a zigzag pattern.

#### Constructor Parameters

```python
SwitchSVGGenerator(
    num_ports=24,                    # Number of normal ports (5-48)
    switch_width=800,                # Width of the switch in pixels
    switch_height=130,               # Height of the switch in pixels
    port_width=28,                   # Width of each port in pixels
    port_height=28,                  # Height of each port in pixels
    port_spacing=4,                  # Spacing between ports in pixels
    legend_spacing=20,               # Spacing between switch body and legend title
    legend_items_spacing=8,          # Spacing between legend title and legend items
    legend_item_padding=3,           # Padding between legend items
    vlan_colors=None,                # Dictionary mapping VLAN IDs to color codes
    port_vlan_map=None,              # Dictionary mapping port numbers to VLAN IDs
    port_status_map=None,            # Dictionary mapping port numbers to their status
    port_labels=None,                # Dictionary mapping port numbers to custom labels
    output_file="switch.svg",        # Path to save the SVG file
    switch_model=SwitchModel.BASIC,  # Model of the switch
    model_name="",                   # Custom model name to display on the switch
    switch_name="",                  # Custom name for the switch
    theme=Theme.LIGHT,               # Color theme
    port_shape=PortShape.SQUARE,     # Shape of the ports
    show_status_indicator=True,      # Whether to show port status indicators
    sfp_ports=0,                     # Number of SFP ports
    sfp_layout="zigzag",             # Layout of SFP ports
    sfp_group_size=0,                # Number of SFP ports per group
    switch_body_color=None,          # Custom color for the switch body
    switch_body_border_color="#000000", # Border color for the switch body
    switch_body_border_width=2,      # Border width for the switch body
    port_group_size=0,               # Number of ports per group
    port_group_spacing=7,            # Additional spacing between port groups
    sfp_only_mode=False              # When True, creates a switch with only SFP ports
)
```

#### Methods

| Method                     | Description                                                               |
|----------------------------|---------------------------------------------------------------------------|
| `save_svg()`               | Generate the SVG and save it to the output file                           |
| `preview_svg()`            | Generate the SVG, save it, and open it in the default web browser         |
| `get_port_color(port_num)` | Get the color for a specific port based on its VLAN assignment and status |
| `get_used_vlans()`         | Get the set of VLANs that are actually used in the port-VLAN mapping      |
| `get_used_statuses()`      | Get the set of port statuses that are actually used                       |

### SingleRowSwitchGenerator Class

The `SingleRowSwitchGenerator` class extends the base generator to create switches with all ports arranged in a single row.

#### Constructor Parameters

The `SingleRowSwitchGenerator` class accepts the same parameters as the `SwitchSVGGenerator` class.

### API Examples

```python
from src.switch_svg_generator import SwitchSVGGenerator, SwitchModel, Theme, PortStatus, PortShape
from src.single_row_switch_generator import SingleRowSwitchGenerator

# Create a basic switch
generator = SwitchSVGGenerator(
    num_ports=24,
    output_file="basic_switch.svg"
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
    switch_body_color="#4a86e8",
    switch_body_border_color="#000000",
    switch_body_border_width=2,
    output_file="enterprise_switch.svg"
)
generator.save_svg()

# Create a single row switch
generator = SingleRowSwitchGenerator(
    num_ports=24,
    sfp_ports=2,
    switch_width=1000,
    switch_height=180,
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Single Row Switch",
    port_labels={1: "WAN", 2: "DMZ", 25: "SFP1", 26: "SFP2"},
    output_file="single_row_switch.svg"
)
generator.save_svg()

# Create an SFP-only switch
generator = SwitchSVGGenerator(
    sfp_ports=8,
    sfp_only_mode=True,
    sfp_layout="horizontal",
    switch_name="SFP-Only Switch",
    output_file="sfp_only_switch.svg"
)
generator.save_svg()
```

## Advanced Customization

### Custom Port Colors

You can customize port colors based on VLAN assignments:

```python
# Define custom VLAN colors
vlan_colors = {
    1: "#3498db",    # Default VLAN - Blue
    10: "#2ecc71",   # Green
    20: "#e74c3c",   # Red
    30: "#f39c12",   # Orange
    40: "#9b59b6",   # Purple
    50: "#1abc9c",   # Turquoise
}

# Assign ports to VLANs
port_vlan_map = {
    1: 10,   # Port 1 on VLAN 10
    2: 10,   # Port 2 on VLAN 10
    3: 20,   # Port 3 on VLAN 20
    4: 20,   # Port 4 on VLAN 20
    5: 30,   # Port 5 on VLAN 30
}

generator = SwitchSVGGenerator(
    num_ports=24,
    vlan_colors=vlan_colors,
    port_vlan_map=port_vlan_map,
    output_file="custom_vlan_colors.svg"
)
```

### Custom Switch Body Styling

You can customize the appearance of the switch body:

```python
generator = SwitchSVGGenerator(
    num_ports=24,
    switch_body_color="#4a86e8",           # Custom blue color
    switch_body_border_color="#000000",    # Black border
    switch_body_border_width=2,            # 2px border width
    output_file="custom_switch_body.svg"
)
```

### Port Grouping

You can group ports with additional spacing between groups:

```python
generator = SwitchSVGGenerator(
    num_ports=24,
    port_group_size=6,        # Group ports in sets of 6
    port_group_spacing=10,    # 10px spacing between groups
    output_file="grouped_ports.svg"
)
```

### Custom Model Names

You can provide a custom model name to display on the switch:

```python
generator = SwitchSVGGenerator(
    num_ports=24,
    switch_model=SwitchModel.ENTERPRISE,
    model_name="Custom Model XYZ-123",    # Custom model name
    output_file="custom_model_name.svg"
)
```

## Examples Gallery

Here are some examples of different switch configurations:

### Port Numbering and Zigzag Pattern Options

```python
# Default: port_start_number=1, zigzag_start_position="top"
generator = SwitchSVGGenerator(
    num_ports=24,
    port_start_number=1,
    zigzag_start_position="top",
    output_file="default_port_numbering.svg"
)

# Start from 0, first port on top
generator = SwitchSVGGenerator(
    num_ports=24,
    port_start_number=0,
    zigzag_start_position="top",
    output_file="start_from_0.svg"
)

# Start from 1, first port on bottom
generator = SwitchSVGGenerator(
    num_ports=24,
    port_start_number=1,
    zigzag_start_position="bottom",
    output_file="first_port_bottom.svg"
)

# Start from 0, first port on bottom
generator = SwitchSVGGenerator(
    num_ports=24,
    port_start_number=0,
    zigzag_start_position="bottom",
    output_file="start_0_bottom.svg"
)
```

### Basic 24-port Switch

```python
generator = SwitchSVGGenerator(
    num_ports=24,
    output_file="basic_24port.svg"
)
```

### Enterprise Switch with Custom VLAN Assignments

```python
generator = SwitchSVGGenerator(
    num_ports=48,
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Core Switch",
    port_vlan_map={1: 10, 2: 10, 3: 20, 4: 20, 5: 30, 6: 30},
    port_status_map={4: PortStatus.DOWN, 8: PortStatus.DISABLED},
    port_labels={1: "WAN", 2: "DMZ", 3: "SRV1", 4: "SRV2"},
    output_file="enterprise_switch.svg"
)
```

### Data Center Switch with Light Theme and Circular Ports

```python
generator = SwitchSVGGenerator(
    num_ports=48,
    switch_model=SwitchModel.DATA_CENTER,
    switch_name="Data Center Switch",
    theme=Theme.LIGHT,
    port_shape=PortShape.CIRCULAR,
    output_file="data_center_switch.svg"
)
```

### Single Row Switch with SFP Ports

```python
generator = SingleRowSwitchGenerator(
    num_ports=24,
    sfp_ports=2,
    switch_width=1000,
    switch_height=180,
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Single Row Switch",
    port_labels={1: "WAN", 2: "DMZ", 25: "SFP1", 26: "SFP2"},
    output_file="single_row_switch.svg"
)
```

### SFP-Only Switch with Horizontal Layout

```python
generator = SwitchSVGGenerator(
    sfp_ports=8,
    sfp_only_mode=True,
    sfp_layout="horizontal",
    switch_name="SFP-Only Switch",
    output_file="sfp_only_switch.svg"
)
```

### Switch with Custom Body Color and Border

```python
generator = SwitchSVGGenerator(
    num_ports=24,
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Custom Colored Switch",
    switch_body_color="#4a86e8",
    switch_body_border_color="#000000",
    switch_body_border_width=2,
    output_file="custom_switch_colors.svg"
)
```

### Switch with Custom Legend Spacing

```python
generator = SwitchSVGGenerator(
    num_ports=24,
    switch_model=SwitchModel.ENTERPRISE,
    switch_name="Switch with Custom Legend Spacing",
    legend_spacing=40,
    legend_items_spacing=30,
    output_file="custom_legend_spacing.svg"
)
