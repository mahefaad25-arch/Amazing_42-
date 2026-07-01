#!/usr/bin/env python3
<<<<<<< HEAD
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   maze_exporter.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bramahef <bramahef@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/29 16:13:53 by bramahef            #+#    #+#            #
#   Updated: 2026/06/29 16:13:54 by bramahef           ###   ########.fr      #
#                                                                             #
# ########################################################################### #
=======
>>>>>>> da8fb51 (alldone and tested)


from typing import Iterable, List, Optional, Tuple
from mazegen import Maze, Cell

WALL_TOP = 1
WALL_RIGHT = 2
WALL_BOTTOM = 4
WALL_LEFT = 8


def encode_cell(cell: Cell) -> int:
    """Return a 4-bit wall mask for a maze cell.

    The mask uses the constants `WALL_TOP`, `WALL_RIGHT`, `WALL_BOTTOM`, and
    `WALL_LEFT` and sets the corresponding bits when the named wall exists.

    Args:
        cell: The `Cell` instance to encode.

    Returns:
        An integer mask (0-15) representing which walls are present.
    """
    value = 0
    if cell.walls["top"]:
        value |= WALL_TOP
    if cell.walls["right"]:
        value |= WALL_RIGHT
    if cell.walls["bottom"]:
        value |= WALL_BOTTOM
    if cell.walls["left"]:
        value |= WALL_LEFT
    return value


def maze_to_hex_lines(maze: Maze) -> List[str]:
    """Encode the maze grid as hexadecimal digits, one string per row.

    Each cell in a row is represented by a single hex digit (0-F) derived
    from `encode_cell`.

    Args:
        maze: The `Maze` instance to serialize.

    Returns:
        A list of strings, one per maze row, where each character is the
        hex representation for the corresponding cell.
    """
    lines: List[str] = []
    for y in range(maze.height):
        row: List[str] = []
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            if cell is None:
                row.append("0")
            else:
                row.append(f"{encode_cell(cell):X}")
        lines.append("".join(row))
    return lines


def path_to_directions(path: Optional[Iterable[Cell]]) -> str:
    """Convert an ordered path of `Cell` objects into NESW direction letters.

    Args:
        path: An iterable of `Cell` objects representing the ordered solution
            path. May be `None` or empty.

    Returns:
        A string composed of the letters `N`, `E`, `S`, `W` describing the
        moves between consecutive cells in `path`. Returns an empty string for
        `None` or empty input. Unknown moves are represented by `?`.
    """
    if not path:
        return ""

    directions: List[str] = []
    previous: Cell | None = None
    for cell in path:
        if previous is None:
            previous = cell
            continue
        dx = cell.x - previous.x
        dy = cell.y - previous.y
        if dx == 1 and dy == 0:
            directions.append("E")
        elif dx == -1 and dy == 0:
            directions.append("W")
        elif dx == 0 and dy == 1:
            directions.append("S")
        elif dx == 0 and dy == -1:
            directions.append("N")
        else:
            directions.append("?")
        previous = cell
    return "".join(directions)


def write_maze_file(
    maze: Maze,
    entry_coords: Tuple[int, int],
    exit_coords: Tuple[int, int],
    solution: Optional[Iterable[Cell]],
    filename: str,
) -> None:
    """Write a maze representation to a text file.

    The file format is:
    - one line per maze row containing hex digits for each cell,
    - a blank line,
    - a line with entry coordinates `x,y`,
    - a line with exit coordinates `x,y`,
    - a line with the solution directions (NESW string).

    Args:
        maze: The `Maze` instance to serialize.
        entry_coords: Tuple (x, y) for the entry cell.
        exit_coords: Tuple (x, y) for the exit cell.
        solution: Optional iterable of `Cell` objects describing the solution
            path (may be `None`).
        filename: Destination filename to write.

    Returns:
        None. Errors are printed to stdout but not propagated.
    """
    lines = maze_to_hex_lines(maze)
    solution_text = path_to_directions(solution)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(f"{line}\n")
            f.write("\n")
            f.write(f"{entry_coords[0]},{entry_coords[1]}\n")
            f.write(f"{exit_coords[0]},{exit_coords[1]}\n")
            f.write(f"{solution_text}\n")
    except Exception as e:
        print(f"Error writing maze file '{filename}': {e}")
