# Configurable Switch Generator

This tool allows you to generate network switch SVG visualizations with configurable layouts and port configurations.

## Features

- Choose between two layout options:
  - **Single Row**: One row with up to 24 normal ports and 2 SFP ports
  - **Double Row**: Two rows (zigzag pattern) with up to 48 normal ports and 6 SFP ports
- Configure the number of normal ports and SFP ports
- Choose between dark and light themes
- Generate SVGs with custom filenames
- Customize spacing between switch body and legend
- Customize spacing between legend title and legend items
- Interactive mode for guided configuration

## Usage

### Command-Line Interface

```bash
# Generate a single row switch with 24 normal ports and 2 SFP ports
python3 configurable_switch_generator.py --layout single --ports 24 --sfp 2

# Generate a double row switch with 48 normal ports and 6 SFP ports
python3 configurable_switch_generator.py --layout double --ports 48 --sfp 6

# Specify a custom output filename
python3 configurable_switch_generator.py --layout single --ports 16 --sfp 2 --output my_switch.svg

# Use light theme
python3 configurable_switch_generator.py --layout double --ports 24 --sfp 4 --theme light

# Provide a custom switch name
python3 configurable_switch_generator.py --layout single --ports 24 --sfp 2 --name "My Custom Switch"

# Customize legend spacing
python3 configurable_switch_generator.py --layout single --ports 24 --sfp 2 --legend-spacing 40 --legend-items-spacing 30
```

### Interactive Mode

For a guided experience, use the interactive mode:

```bash
python3 configurable_switch_generator.py --interactive
```

This will prompt you for:
1. Layout type (single or double row)
2. Number of normal ports
3. Number of SFP ports
4. Output filename
5. Theme (dark or light)

### Command-Line Options

| Option | Description |
|--------|-------------|
| `--layout {single,double}` | Layout type: single for one row, double for two rows (zigzag) |
| `--ports N` | Number of normal ports (1-24 for single, 1-48 for double) |
| `--sfp N` | Number of SFP ports (0-2 for single, 0-6 for double) |
| `--output FILENAME` | Output SVG filename |
| `--name NAME` | Custom switch name |
| `--theme {dark,light}` | Color theme (default: dark) |
| `--legend-spacing N` | Spacing between switch body and legend title in pixels |
| `--legend-items-spacing N` | Spacing between legend title and legend items in pixels |
| `--interactive` | Run in interactive mode (prompts for input) |

## Examples

### Single Row Switch (24 ports, 2 SFP)

![Single Row Switch](single_row_switch_24p_2sfp.svg)

### Double Row Switch (48 ports, 6 SFP)

![Double Row Switch](double_row_switch_48p_6sfp.svg)

## How It Works

The script uses two different generator classes:

1. `SingleRowSwitchGenerator`: Places all ports in a single row
2. `SwitchSVGGenerator`: Places ports in a zigzag pattern (double row)

Based on your selected layout type, the script uses the appropriate generator and configures it with the specified parameters.
