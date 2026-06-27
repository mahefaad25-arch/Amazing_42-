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


def format_solution(path: Optional[Iterable[Cell]]) -> str:
    """Format the solver path as a simple coordinate string."""
    if not path:
        return ""
    return " ".join(f"{cell.x},{cell.y}" for cell in path)


def write_maze_file(
    maze: Maze,
    entry_coords: Tuple[int, int],
    exit_coords: Tuple[int, int],
    solution: Optional[Iterable[Cell]],
    filename: str,
) -> None:
    """Write a maze file with hex cell codes, entry, exit, and solution."""
    lines = maze_to_hex_lines(maze)
    solution_text = format_solution(solution)
    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(f"{line}\n")
        f.write(f"{entry_coords[0]},{entry_coords[1]}\n")
        f.write(f"{exit_coords[0]},{exit_coords[1]}\n")
        f.write(f"{solution_text}\n")
