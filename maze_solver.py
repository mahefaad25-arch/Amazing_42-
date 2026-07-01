#!/usr/bin/env python3

from collections import deque
from typing import List, Optional, Tuple, Any
from mazegen import Maze, Cell


class MazeSolver:
    """Handles finding a path from start to end in a Maze object.

    This class provides maze-solving utilities, currently implemented with a
    breadth-first search (BFS) approach implemented iteratively to avoid
    recursion depth issues.
    """

    def __init__(self, maze: Maze) -> None:
        """Initialize the solver with a maze instance.

        Args:
            maze: The `Maze` object to solve.
        """
        self.maze = maze

    def solve(
        self,
        start_coords: Tuple[int, int] = (0, 0),
        end_coords: Optional[Tuple[int, int]] = None,
    ) -> List[Cell]:
        """Find a path from `start_coords` to `end_coords` using BFS.

        The search explores neighbors in the order: top, right, bottom, left
        and respects cell walls. Returned path is an ordered list of `Cell`
        objects from start to end inclusive. If no path exists, an empty list
        is returned.

        Args:
            start_coords: Tuple `(x, y)` for the start cell.
            Defaults to (0, 0).
            end_coords: Optional tuple `(x, y)` for the end cell.
            If `None`, the
                bottom-right corner of the maze is used.

        Returns:
            A list of `Cell` instances representing the path from start to
            end. Returns an empty list if start/end are invalid or no path is
            found.
        """
        if end_coords is None:
            end_coords = (self.maze.width - 1, self.maze.height - 1)

        start_cell = self.maze.get_cell(*start_coords)
        end_cell = self.maze.get_cell(*end_coords)

        if not start_cell or not end_cell:
            return []
        stack = deque([start_cell])
        visited_in_solving = {start_cell}
        parent_map: dict[Cell, Any] = {start_cell: None}

        found = False
        while stack:
            current = stack.popleft()

            if current == end_cell:
                found = True
                break

            directions = [
                ((current.x, current.y - 1), "top", "bottom"),
                ((current.x + 1, current.y), "right", "left"),
                ((current.x, current.y + 1), "bottom", "top"),
                ((current.x - 1, current.y), "left", "right"),
            ]

            for (nx, ny), wall_current, wall_neighbor in directions:
                neighbor = self.maze.get_cell(nx, ny)
                if neighbor and neighbor not in visited_in_solving:
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
