#!/usr/bin/env python3

"""maze: Cell and Maze classes for grid management and ASCII/ANSI rendering.

This module provides the `Cell` and `Maze` classes used by the
generator (`maze_generator.py`) and the solver (`maze_solver.py`).
The `display` method provides rich console rendering (blocks/path).
"""

from typing import List, Optional


class Cell:
    """Single cell in the maze grid with four walls and visited flag.

    Attributes:
        x: X coordinate (column) of the cell.
        y: Y coordinate (row) of the cell.
        visited: Bool indicating whether the cell has been visited by the
            generator algorithm.
        is_center_42: Bool marking whether the cell is part of the reserved
            central "42" pattern.
        walls: Dict mapping wall names ("top", "right", "bottom", "left")
            to booleans indicating presence of each wall.
    """

    def __init__(self, x: int, y: int) -> None:
        """Create a new `Cell` at the given coordinates.

        Args:
            x: Column index of the cell.
            y: Row index of the cell.
        """
        self.x = x
        self.y = y
        self.visited = False
        self.is_center_42 = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}


class Maze:
    """Grid container: access cells and render a compact console view.

    Notes:
    - `grid[x][y]` stores `Cell` objects.
    - Rendering uses ANSI blocks for clearer visual output in terminals
      that support colors/attributes.
    """

    def __init__(self, width: int, height: int) -> None:
        """Create a maze grid of the requested size.

        Args:
            width: Number of columns in the maze.
            height: Number of rows in the maze.
        """
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """Return the maze cell at the given coordinates.

        Args:
            x: Column index of the requested cell.
            y: Row index of the requested cell.

        Returns:
            The Cell instance at (x, y), or None if the coordinates are out of
            bounds.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        return None

    def display(
        self,
        path: Optional[List[Cell]] = None,
        entry_coords: Optional[tuple[int, int]] = None,
        exit_coords: Optional[tuple[int, int]] = None,
    ) -> None:
        """Render the maze to the terminal with path highlighting.

        `path` may be a list of `Cell` objects;
        `entry_coords` and `exit_coords` allow
        marking the configured start/end.

        Args:
            path: Optional list of `Cell` objects to highlight as the path.
            entry_coords: Optional `(x, y)` tuple marking the start cell.
            exit_coords: Optional `(x, y)` tuple marking the end cell.

        Returns:
            None. The maze is printed to stdout.
        """
        path_set = set(path) if path else set()
        entry_cell = (
            self.get_cell(*entry_coords) if entry_coords is not None else None
        )
        exit_cell = (
            self.get_cell(*exit_coords) if exit_coords is not None else None
        )

        r_width = self.width * 2 + 1
        r_height = self.height * 2 + 1

        grid = [["█" for _ in range(r_width)] for _ in range(r_height)]

        for x in range(self.width):
            for y in range(self.height):
                cell = self.grid[x][y]
                cx, cy = x * 2 + 1, y * 2 + 1

                if cell is entry_cell:
                    grid[cy][cx] = "S"
                elif cell is exit_cell:
                    grid[cy][cx] = "E"
                elif cell in path_set:
                    grid[cy][cx] = "·"
                else:
                    grid[cy][cx] = " "

                if not cell.walls["top"] and y > 0:
                    top_cell = self.grid[x][y - 1]
                    is_path = cell in path_set and top_cell in path_set
                    grid[cy - 1][cx] = "·" if is_path else " "

                if not cell.walls["bottom"] and y < self.height - 1:
                    bot_cell = self.grid[x][y + 1]
                    is_path = cell in path_set and bot_cell in path_set
                    grid[cy + 1][cx] = "·" if is_path else " "

                if not cell.walls["left"] and x > 0:
                    left_cell = self.grid[x - 1][y]
                    is_path = cell in path_set and left_cell in path_set
                    grid[cy][cx - 1] = "·" if is_path else " "

                if not cell.walls["right"] and x < self.width - 1:
                    right_cell = self.grid[x + 1][y]
                    is_path = cell in path_set and right_cell in path_set
                    grid[cy][cx + 1] = "·" if is_path else " "

        for row in grid:
            line_str = ""
            for char in row:
                if char == "█":
                    line_str += "\033[40m  \033[0m"
                elif char == "·":
                    line_str += "\033[47m\033[31m··\033[0m"
                elif char == "S":
                    line_str += "\033[42m\033[30mSS\033[0m"
                elif char == "E":
                    line_str += "\033[44m\033[97mEE\033[0m"
                else:
                    line_str += "\033[47m  \033[0m"
            print(line_str)
