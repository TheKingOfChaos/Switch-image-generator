# Network Switch SVG Generator

A tool for generating SVG visualizations of network switches with configurable layouts and port configurations.

## Project Structure

```
switch_grafic_generator/
├── src/                  # Source code
│   ├── switch_svg_generator.py         # Base generator class with layout options
│   ├── single_row_switch_generator.py  # Legacy class maintained for backward compatibility
│   ├── configurable_switch_generator.py # Configurable generator with CLI
│   └── generate_switch.py              # Internal entry point
├── examples/             # Example scripts
│   ├── create_single_row_switch.py     # Example of single row switch
│   ├── create_sfp_only_switch.py       # Example of SFP-only switch
│   ├── example_layout_modes.py         # Example of different layout modes
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

## Features

- Generate network switch SVG visualizations with different layouts:
  - Single row layout with up to 24 normal ports and 2 SFP ports
  - Double row (zigzag) layout with up to 48 normal ports and 6 SFP ports
  - SFP-only mode with 4-32 SFP ports and no regular ports
- Choose layout mode directly in the SwitchSVGGenerator class:
  - Use `layout_mode=LayoutMode.ZIGZAG` for the traditional zigzag layout (default)
  - Use `layout_mode=LayoutMode.SINGLE_ROW` for a single row layout
- Flexible SFP port layout options:
  - Zigzag layout (default) - SFP ports in a zigzag pattern (similar to regular ports)
  - Horizontal layout - All SFP ports in a single horizontal row
- Group ports with additional spacing between groups (both regular and SFP ports)
- Customize port colors based on VLAN assignments
- Set port status (up/down/disabled)
- Add custom port labels
- Choose between dark and light themes
- Place legend inside or outside the switch
- Customize spacing between switch body and legend
- Customize spacing between legend title and legend items

## Quick Start

### Using the Command-Line Interface

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

### Using the Python API

```python
from src.switch_svg_generator import SwitchSVGGenerator, LayoutMode, SwitchModel, Theme

# Create a switch with zigzag layout (default)
generator = SwitchSVGGenerator(
    num_ports=48,
    sfp_ports=6,
    output_file="zigzag_switch.svg"
)
generator.save_svg()

# Create a switch with single row layout
generator = SwitchSVGGenerator(
    num_ports=24,
    sfp_ports=2,
    layout_mode=LayoutMode.SINGLE_ROW,
    output_file="single_row_switch.svg"
)
generator.save_svg()

# Create an SFP-only switch
generator = SwitchSVGGenerator(
    sfp_ports=8,
    sfp_only_mode=True,
    output_file="sfp_only_switch.svg"
)
generator.save_svg()
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

## Examples

Check the `examples/` directory for sample scripts demonstrating different configurations.

To run an example:

```bash
python3 examples/example_layout_modes.py
```

## Documentation

For more detailed documentation, see:

- [Comprehensive Documentation](docs/COMPREHENSIVE_DOCUMENTATION.md)
- [Configurable Switch Documentation](docs/CONFIGURABLE_SWITCH_README.md)
- [Single Row Switch Documentation](docs/SINGLE_ROW_SWITCH_README.md)
