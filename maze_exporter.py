#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   maze_exporter.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: GitHub Copilot <copilot@example.com>          +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/26 15:00:00 by copilot            #+#    #+#            #
#   Updated: 2026/06/26 15:00:00 by copilot           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from typing import Iterable, List, Optional, Tuple
from maze import Maze, Cell

WALL_TOP = 1
WALL_RIGHT = 2
WALL_BOTTOM = 4
WALL_LEFT = 8


def encode_cell(cell: Cell) -> int:
    """Return a 4-bit wall mask for a maze cell."""
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
    """Encode the maze grid as hex digits row by row."""
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
    """Convert an ordered path of cells into NESW directions."""
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
            # Non-adjacent cells should not happen for a valid path.
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
    """Write a maze file with hex cell codes, entry, exit, and solution."""
    lines = maze_to_hex_lines(maze)
    solution_text = path_to_directions(solution)
    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(f"{line}\n")
        f.write("\n")
        f.write(f"{entry_coords[0]},{entry_coords[1]}\n")
        f.write(f"{exit_coords[0]},{exit_coords[1]}\n")
        f.write(f"{solution_text}\n")
