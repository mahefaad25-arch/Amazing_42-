#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   maze_generator.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bramahef <bramahef@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/23 07:42:42 by loandria            #+#    #+#            #
#   Updated: 2026/06/25 16:30:06 by bramahef           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import random
from maze import Maze, Cell
from typing import List, Tuple


class MazeGenerator:
    """Handles the generation of paths within a Maze object."""

    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def get_unvisited_neighbors(self, cell: Cell) -> List[Cell]:
        """Find and return all adjacent cells that have not been visited."""
        neighbors = []
        top = self.maze.get_cell(cell.x, cell.y - 1)
        if top and not top.visited:
            neighbors.append(top)
        right = self.maze.get_cell(cell.x + 1, cell.y)
        if right and not right.visited:
            neighbors.append(right)
        bottom = self.maze.get_cell(cell.x, cell.y + 1)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        left = self.maze.get_cell(cell.x - 1, cell.y)
        if left and not left.visited:
            neighbors.append(left)
        return neighbors

    def remove_walls(self, current: Cell, next_cell: Cell) -> None:
        """Break down the shared walls between two adjacent cells."""
        dx = current.x - next_cell.x
        dy = current.y - next_cell.y
        if dx == 1:
            current.walls["left"] = False
            next_cell.walls["right"] = False
        elif dx == -1:
            current.walls["right"] = False
            next_cell.walls["left"] = False
        elif dy == 1:
            current.walls["top"] = False
            next_cell.walls["bottom"] = False
        elif dy == -1:
            current.walls["bottom"] = False
            next_cell.walls["top"] = False

    def generate(self, start_coords: Tuple[int, int] = (0, 0)) -> None:
        """Generate the paths using a randomized depth-first search from start_coords."""
        start_cell = self.maze.get_cell(*start_coords)
        if not start_cell:
            return
        stack = [start_cell]
        start_cell.visited = True
        while stack:
            current = stack[-1]
            neighbors = self.get_unvisited_neighbors(current)
            if neighbors:
                random.shuffle(neighbors)
                next_cell = neighbors[0]
                self.remove_walls(current, next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()
