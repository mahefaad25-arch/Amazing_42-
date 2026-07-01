*This project has been created as part of the 42 curriculum by loandria, bramahef.*

# A-Maze-ing: Interactive Maze Generator and Solver

## Description

A-Maze-ing is a Python project that generates, solves, and displays mazes using a combination of console and graphical output. The goal is to build a maze engine with:
- configurable size and entry/exit positions,
- a perfect maze generator,
- optional imperfect maze generation with loops,
- a solver that finds the shortest path from entry to exit,
- an interactive MiniLibX-based GUI for exploring the maze.

The project was created to demonstrate maze generation algorithms, pathfinding, config parsing, and graphical interaction in a single structured application.

## Instructions

### Installation

```bash
make install
source .venv/bin/activate
```

### Execution

Create or edit `config.txt` and run the main script:

```bash
make run
# or
python3 a_maze_ing.py config.txt
```

### Build and lint

```bash
make lint
make flake
make clean
make fclean
make re
```

## Config file format

The config file is a plain text file with one setting per line in the format `key=value`.
Keys are case-insensitive.

Required settings:
- `width`: maze width as a positive integer
- `height`: maze height as a positive integer
- `entry`: entry coordinates as `x,y`
- `exit`: exit coordinates as `x,y`
- `output_file`: path to the exported maze file

Optional settings:
- `perfect`: `true` or `false` (default: `true`)
- `seed`: optional integer seed for reproducible generation

Example:

```
width=20
height=20
entry=2,10
exit=10,10
output_file=maze.txt
perfect=false
seed=4
```

## Algorithm choice

### Maze generation

This project uses a randomized depth-first search algorithm to generate perfect mazes. The algorithm was chosen because:
- it produces a single valid path between any two cells,
- it is easy to implement with backtracking,
- it supports deterministic behavior using a seed,
- it allows controlled addition of loops for imperfect mazes.

The implementation also protects a reserved "42" pattern in the center of mazes 12×12 or larger, and optionally injects random loops when `perfect=false`.

### Maze solving

The solver uses breadth-first search (BFS) to compute the shortest path from entry to exit. BFS was chosen because it guarantees the shortest path in an unweighted grid and is simple to trace back to the start.

## Reusability

The code is modular and reusable in other projects:
- `mazegen/maze.py`: reusable grid and cell model for any maze-based application
- `mazegen/maze_generator.py`: generic BFS-based maze generator with optional loops
- `maze_solver.py`: reusable BFS pathfinding on a grid of cells
- `maze_exporter.py`: reusable maze export format for file-based output
- `maze_interface.py`: reusable MiniLibX rendering and input handler for maze visualization

## Project structure

```
maze/
├── main.py               # application entry point
├── config.txt            # default configuration example
├── config_parser.py      # parser and validator for config files
├── maze_interface.py     # MiniLibX interface and keyboard handling
├── maze_solver.py        # BFS solver for the maze
├── maze_exporter.py      # file export for maze output
├── maze_animation.py     # optional path animation utilities
├── Makefile              # build/run/lint tasks
├── requirements.txt      # Python dependencies
├── pyproject.toml        # packaging metadata for mlx dependency
└── mazegen/
    ├── __init__.py
    ├── maze.py           # maze grid and cell classes
    └── maze_generator.py # BFS maze generator with 42-pattern reservation
```

## Resources

- "Maze generation algorithms" - Wikipedia
- "Breadth-first search" - Graph traversal tutorial
- MiniLibX Python binding documentation
- 42 School coding standards and project requirements

### AI usage

AI assistance was used for:
- renaming project files and updating imports,
- cleaning up code and adding type annotations,
- generating the README content and project documentation.

## Contributors

- **loandria** - Primary developer
- **bramahef** - Co-developer


### Planning

Initial planning focused on:
- config-driven maze generation,
- generator and solver separation,
- GUI interaction and export support.

The plan evolved to include:
- `perfect=true` default behavior,
- optional `seed` support,
- central `42` pattern protection,
- more coherent file naming and documentation.

### What worked well

- modular design with separate generator, solver, parser, and GUI
- strict type checking with `mypy`
- consistent command flow through `Makefile`

### Improvements

- add multiple maze generation algorithms
- improve the exporter with more output formats
- formal test suite for parser and solver

### Tools used

- Python 3
- `make` for project tasks
- `venv` for dependency isolation
- `flake8` for linting
- `mypy` for static typing
- MiniLibX for graphical display
