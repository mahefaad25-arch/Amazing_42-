#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   solver.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: loandria <loandria@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/23 07:42:26 by loandria            #+#    #+#            #
#   Updated: 2026/06/26 01:20:31 by loandria           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from typing import List, Optional, Tuple
from maze import Maze, Cell


class MazeSolver:
    """Handles finding a path from start to end in a Maze object."""

    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def solve(
        self,
        start_coords: Tuple[int, int] = (0, 0),
        end_coords: Optional[Tuple[int, int]] = None,
    ) -> List[Cell]:
        """Solve the maze using an iterative DFS
        algorithm to avoid RecursionError."""
        if end_coords is None:
            end_coords = (self.maze.width - 1, self.maze.height - 1)

        start_cell = self.maze.get_cell(*start_coords)
        end_cell = self.maze.get_cell(*end_coords)

        if not start_cell or not end_cell:
            return []
        stack = [start_cell]
        visited_in_solving = {start_cell}

        # Dictionnaire pour retrouver le chemin (parent de chaque cellule)
        parent_map: dict[Cell, Optional[Cell]] = {start_cell: None}

        found = False
        while stack:
            current = stack.pop()

            if current == end_cell:
                found = True
                break

            # Définition des directions adjacentes
            directions = [
                ((current.x, current.y - 1), "top", "bottom"),
                ((current.x + 1, current.y), "right", "left"),
                ((current.x, current.y + 1), "bottom", "top"),
                ((current.x - 1, current.y), "left", "right"),
            ]

            for (nx, ny), wall_current, wall_neighbor in directions:
                neighbor = self.maze.get_cell(nx, ny)
                if neighbor and neighbor not in visited_in_solving:
                    # Vérifier s'il n'y a pas de mur entre les deux cellules
                    if (
                        not current.walls[wall_current]
                        and not neighbor.walls[wall_neighbor]
                    ):
                        visited_in_solving.add(neighbor)
                        parent_map[neighbor] = current
                        stack.append(neighbor)

        if found:
            path = []
            curr = end_cell
            while curr is not None:
                path.append(curr)
                curr = parent_map[curr]
            path.reverse()
            return path

        return []
