#!/usr/bin/env python3
"""Configuration file parser utilities.

This module provides helpers to read a simple key=value configuration file
used by the maze generator. It validates required keys, converts values to
appropriate types, and performs basic bounds/consistency checks.
"""

import sys
from typing import Dict, Any


def is_in_42_pattern(x: int, y: int, width: int, height: int) -> bool:
    """Check if coordinates are within the reserved 42 pattern area."""
    center_x = width // 2
    center_y = height // 2

    wall_42 = {
        (-3, -2), (-3, -1), (-3, 0), (-2, 0), (-1, -2), (-1, -1),
        (-1, 0), (-1, 1), (-1, 2),
        (1, -2), (2, -2), (3, -2), (3, -1),
        (1, 0), (2, 0), (3, 0), (1, 1), (1, 2), (2, 2), (3, 2)
    }

    dx = x - center_x
    dy = y - center_y
    return (dx, dy) in wall_42


def config_parser(filename: str) -> Dict[str, Any]:
    """Parse a simple configuration file into a dictionary.

    The configuration file is expected to contain lines in the form
    `key = value`. Supported keys are `width`, `height`, `entry`, `exit`,
    `perfect`, `seed`, and `output_file`.

    Args:
        filename: Path to the configuration file to read.

    Returns:
        A dictionary with parsed and type-converted configuration values.

    Exits:
        The function will call `sys.exit(1)` when the file is missing,
        unreadable, malformed, or semantically invalid (missing required
        keys, out-of-bounds coordinates, etc.).
    """

    config: Dict[str, Any] = {}

    allowed_keys = {
        "width",
        "height",
        "entry",
        "exit",
        "perfect",
        "seed",
        "output_file",
    }

    try:
        with open(filename, "r") as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    print(f"Error line {line_num}: missing '='.")
                    sys.exit(1)

                key, value = line.split("=", 1)
                key = key.strip().lower()
                value = value.strip()

                if key not in allowed_keys:
                    print(f"Error line {line_num}: unknown key '{key}'.")
                    sys.exit(1)

                if key in config:
                    print(f"Key '{key}' already defined.")
                    sys.exit(1)

                try:
                    if key in ["width", "height"]:
                        config[key] = int(value)
                        if config[key] <= 0:
                            raise ValueError(f"{key} must be greater than 0")

                    elif key in ["entry", "exit"]:
                        parts = value.split(",")

                        if len(parts) != 2:
                            raise ValueError("expected format: x,y")

                        x, y = map(int, parts)

                        if x < 0 or y < 0:
                            raise ValueError(f"{key} cannot be negative")

                        config[key] = (x, y)

                    elif key == "perfect":
                        if value.lower() == "true":
                            config[key] = True
                        elif value.lower() == "false":
                            config[key] = False
                        else:
                            raise ValueError("perfect must be True or False")

                    elif key == "seed":
                        config[key] = int(value)
                        if config[key] < 0:
                            raise ValueError("seed cannot be negative")

                    elif key == "output_file" and value != "":
                        config[key] = value

                except ValueError as e:
                    print(f"Error line {line_num}: {e}")
                    sys.exit(1)

    except FileNotFoundError:
        print(f"Error: file '{filename}' not found.")
        sys.exit(1)

    except PermissionError:
        print(f"Error: insufficient permissions to read '{filename}'.")
        sys.exit(1)
    mandatory_keys = ["width", "height", "entry", "exit"]
    missing = [k for k in mandatory_keys if k not in config]

    if missing:
        print("Configuration error: missing keys: " + ", ".join(missing))
        sys.exit(1)

    config.setdefault("perfect", True)
    config.setdefault("seed", None)
    config.setdefault("output_file", "optional_maze.txt")

    width = config["width"]
    height = config["height"]
    entry_x, entry_y = config["entry"]
    exit_x, exit_y = config["exit"]
    if width * height > 1000:
        print(
            f"Warning: maze size {width}x{height} is large; "
            "generation may take a while."
        )
    if not (0 <= entry_x < width and 0 <= entry_y < height):
        print(f"Interface error: entry {config['entry']} out of bounds.")
        sys.exit(1)

    if not (0 <= exit_x < width and 0 <= exit_y < height):
        print(f"Interface error: exit {config['exit']} out of bounds.")
        sys.exit(1)

    if config["entry"] == config["exit"]:
        print("Interface error: entry and exit must differ.")
        sys.exit(1)

    if width >= 12 and height >= 12:
        if is_in_42_pattern(entry_x, entry_y, width, height):
            print(f"Error: entry {config['entry']} is in 42 pattern.")
            sys.exit(1)

        if is_in_42_pattern(exit_x, exit_y, width, height):
            print(f"Error: exit {config['exit']} is in 42 pattern.")
            sys.exit(1)

    else:
        print("Warning: maze too small for 42 pattern (min 12x12).")

    return config


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 config_parser.py config.txt")
        sys.exit(1)

    parsed_config = config_parser(sys.argv[1])
    print("Configuration loaded successfully:", parsed_config)
