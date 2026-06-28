#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   maze_generator.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bramahef <bramahef@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/23 07:42:42 by loandria            #+#    #+#            #
#   Updated: 2026/06/28 11:14:22 by bramahef           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import random
from maze import Maze, Cell
from typing import List, Tuple


class MazeGenerator:
    """Handles the generation of paths within a Maze object."""

    def __init__(self, maze: Maze, seed: int | None = None, perfect: bool = True) -> None:
        self.maze = maze
        self.rng = random.Random(seed)
        self.perfect = perfect

    def _reset_visited(self) -> None:
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                cell = self.maze.get_cell(x, y)
                if cell:
                    cell.visited = cell.is_center_42

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

    def reserve_center_42(self) -> None:
        center_x = self.maze.width // 2
        center_y = self.maze.height // 2

        wall_42 = {
            (-3, -2), (-3, -1), (-3, 0), (-2, 0), (-1, -2), (-1, -1),
            (-1, 0), (-1, 1), (-1, 2),
            (1, -2), (2, -2), (3, -2), (3, -1),
            (1, 0), (2, 0), (3, 0), (1, 1), (1, 2), (2, 2), (3, 2)
        }

        for dy in range(-3, 4):
            for dx in range(-5, 6):
                if (dx, dy) in wall_42:
                    cell = self.maze.get_cell(center_x + dx, center_y + dy)
                    if cell:
                        cell.visited = True
                        cell.is_center_42 = True
                        cell.walls["top"] = True
                        cell.walls["bottom"] = True
                        cell.walls["left"] = True
                        cell.walls["right"] = True

    def _build_perfect_maze(self, start_cell: Cell) -> None:
        start_cell.visited = True
        stack = [start_cell]
        while stack:
            current = stack[-1]
            neighbors = []
            directions = [
                ((current.x, current.y - 1), "top", "bottom"),
                ((current.x + 1, current.y), "right", "left"),
                ((current.x, current.y + 1), "bottom", "top"),
                ((current.x - 1, current.y), "left", "right"),
            ]
            for (nx, ny), wall_current, wall_neighbor in directions:
                neighbor = self.maze.get_cell(nx, ny)
                if neighbor and not neighbor.visited:
                    if self._can_open_wall(current, neighbor, wall_current, wall_neighbor):
                        neighbors.append((neighbor, wall_current, wall_neighbor))

            if neighbors:
                self.rng.shuffle(neighbors)
                next_cell, wall_current, wall_neighbor = neighbors[0]
                self.remove_walls(current, next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

    def _has_forbidden_open_area(self) -> bool:
        if self.maze.width < 3 or self.maze.height < 3:
            return False

        for x in range(self.maze.width - 2):
            for y in range(self.maze.height - 2):
                full_open = True
                for dx in range(3):
                    for dy in range(3):
                        cell = self.maze.get_cell(x + dx, y + dy)
                        if dx < 2:
                            right = self.maze.get_cell(x + dx + 1, y + dy)
                            if cell.walls["right"] or right.walls["left"]:
                                full_open = False
                                break
                        if dy < 2:
                            bottom = self.maze.get_cell(x + dx, y + dy + 1)
                            if cell.walls["bottom"] or bottom.walls["top"]:
                                full_open = False
                                break
                    if not full_open:
                        break
                if full_open:
                    return True
        return False

    def _can_open_wall(self, current: Cell, neighbor: Cell, wall_current: str, wall_neighbor: str) -> bool:
        if not current.walls[wall_current] or not neighbor.walls[wall_neighbor]:
            return False

        current.walls[wall_current] = False
        neighbor.walls[wall_neighbor] = False
        forbidden = self._has_forbidden_open_area()
        current.walls[wall_current] = True
        neighbor.walls[wall_neighbor] = True
        return not forbidden

    def _add_random_loops(self) -> None:
        candidates: List[tuple[Cell, Cell, str, str]] = []
        directions = [
            ((1, 0), "right", "left"),
            ((0, 1), "bottom", "top"),
        ]

        for x in range(self.maze.width):
            for y in range(self.maze.height):
                current = self.maze.get_cell(x, y)
                if not current or current.is_center_42:
                    continue
                for (dx, dy), wall_current, wall_neighbor in directions:
                    neighbor = self.maze.get_cell(x + dx, y + dy)
                    if not neighbor or neighbor.is_center_42:
                        continue
                    if current.walls[wall_current] and neighbor.walls[wall_neighbor]:
                        candidates.append((current, neighbor, wall_current, wall_neighbor))

        self.rng.shuffle(candidates)
        target = max(1, (self.maze.width * self.maze.height) // 20)
        loops = 0
        for current, neighbor, wall_current, wall_neighbor in candidates:
            if loops >= target:
                break
            if self._can_open_wall(current, neighbor, wall_current, wall_neighbor):
                self.remove_walls(current, neighbor)
                loops += 1

    def generate(self, start_coords: Tuple[int, int] = (0, 0)) -> None:
        """Generate the paths using a randomized
          depth-first search from start_coords."""
        self._reset_visited()
        if self.maze.width >= 12 and self.maze.height >= 12:
            self.reserve_center_42()

        start_cell = self.maze.get_cell(*start_coords)
        if not start_cell:
            return

        self._build_perfect_maze(start_cell)

        if not self.perfect:
            self._add_random_loops()
