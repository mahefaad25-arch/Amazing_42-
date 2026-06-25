#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   maze.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bramahef <bramahef@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/23 07:42:09 by loandria            #+#    #+#            #
#   Updated: 2026/06/25 17:07:36 by bramahef           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""maze: Cell and Maze classes for grid management and ASCII/ANSI rendering.

Ce module fournit les classes `Cell` et `Maze` utilisées par le
générateur (`maze_generator.py`) et le solveur (`maze_solver.py`).
La méthode `display` offre un rendu console riche (blocs/chemin).
"""

from typing import List, Optional, Tuple


# # maze.py
class Cell:
    """Single cell in the maze grid with four walls and visited flag."""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}


class Maze:
    """Grid container: access cells and render a compact console view.

    Notes:
    - `grid[x][y]` stores `Cell` objects.
    - Rendering uses ANSI blocks for clearer visual output in terminals
      that support colors/attributes.
    """

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        return None

    def display(self, path: Optional[List[Cell]] = None) -> None:
        """Render the maze to the terminal with path highlighting.

        `path` may be a list of `Cell` objects; celles du chemin seront marquées.
        """
        path_set = set(path) if path else set()
        r_width = self.width * 2 + 1
        r_height = self.height * 2 + 1

        grid = [["█" for _ in range(r_width)] for _ in range(r_height)]

        for x in range(self.width):
            for y in range(self.height):
                cell = self.grid[x][y]
                cx, cy = x * 2 + 1, y * 2 + 1

                grid[cy][cx] = "·" if cell in path_set else " "

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

        grid[0][1] = "·" if self.grid[0][0] in path_set else " "
        exit_x, exit_y = self.width - 1, self.height - 1
        grid[r_height - 1][r_width - 2] = (
            "·" if self.grid[exit_x][exit_y] in path_set else " "
        )

        for row in grid:
            line_str = ""
            for char in row:
                if char == "█":
                    line_str += "\033[40m  \033[0m"
                elif char == "·":
                    line_str += "\033[47m\033[31m··\033[0m"
                else:
                    line_str += "\033[47m  \033[0m"
            print(line_str)
