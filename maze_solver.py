from maze import Maze, Cell
from typing import List, Optional, Tuple


class MazeSolver:
    """Handles finding a path from start to end in a Maze object."""

    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def solve(
        self,
        start_coords: Tuple[int, int] = (0, 0),
        end_coords: Optional[Tuple[int, int]] = None
    ) -> List[Cell]:
        """Solve the maze using a DFS algorithm and return the path."""
        if end_coords is None:
            end_coords = (self.maze.width - 1, self.maze.height - 1)

        start_cell = self.maze.get_cell(*start_coords)
        end_cell = self.maze.get_cell(*end_coords)

        if not start_cell or not end_cell:
            return []

        visited_in_solving = set()
        path = []

        def dfs(current: Cell) -> bool:
            if current == end_cell:
                path.append(current)
                return True

            visited_in_solving.add(current)
            path.append(current)

            directions = [
                ((current.x, current.y - 1), 'top', 'bottom'),
                ((current.x + 1, current.y), 'right', 'left'),
                ((current.x, current.y + 1), 'bottom', 'top'),
                ((current.x - 1, current.y), 'left', 'right')
            ]

            for (nx, ny), wall_current, wall_neighbor in directions:
                neighbor = self.maze.get_cell(nx, ny)
                if neighbor and neighbor not in visited_in_solving:
                    if (not current.walls[wall_current]
                            and not neighbor.walls[wall_neighbor]):
                        if dfs(neighbor):
                            return True

            path.pop()
            return False

        if dfs(start_cell):
            return path
        return []
