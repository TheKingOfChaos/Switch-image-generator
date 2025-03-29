# Network Switch SVG Generator

A tool for generating SVG visualizations of network switches with configurable layouts and port configurations.

## Project Structure

```
switch_grafic_generator/
├── src/                  # Source code
│   ├── switch_svg_generator.py         # Base generator class
│   ├── single_row_switch_generator.py  # Single row layout generator
│   └── configurable_switch_generator.py # Configurable generator with CLI
├── examples/             # Example scripts
│   ├── create_single_row_switch.py     # Example of single row switch
│   ├── one_row_switch_with_sfp.py      # Example using base generator
│   └── ...                             # Other examples
├── docs/                 # Documentation
│   ├── README.md                       # Original README
│   ├── CONFIGURABLE_SWITCH_README.md   # Configurable switch documentation
│   └── SINGLE_ROW_SWITCH_README.md     # Single row switch documentation
├── output/               # Generated SVG files
│   └── ...                             # SVG output files
└── generate_switch.py    # Main script
```

## Features

- Generate network switch SVG visualizations with different layouts:
  - Single row layout with up to 24 normal ports and 2 SFP ports
  - Double row (zigzag) layout with up to 48 normal ports and 6 SFP ports
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

# Use interactive mode for guided configuration
./generate_switch.py --interactive
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `--layout {single,double}` | Layout type: single for one row, double for two rows (zigzag) |
| `--ports N` | Number of normal ports (1-24 for single, 1-48 for double) |
| `--sfp N` | Number of SFP ports (0-2 for single, 0-6 for double) |
| `--output FILENAME` | Output SVG filename |
| `--name NAME` | Custom switch name |
| `--theme {dark,light}` | Color theme (default: dark) |
| `--interactive` | Run in interactive mode (prompts for input) |

## Examples

Check the `examples/` directory for sample scripts demonstrating different configurations.

To run an example:

```bash
python3 examples/create_single_row_switch.py
```

## Documentation

For more detailed documentation, see:

- [Configurable Switch Documentation](docs/CONFIGURABLE_SWITCH_README.md)
- [Single Row Switch Documentation](docs/SINGLE_ROW_SWITCH_README.md)
