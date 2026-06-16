import random
import re
import sys
from typing import List, Optional, Tuple


class Cell:
    """Represent a single cell in the maze grid."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize a cell with coordinates and default walls."""
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {
            'top': True,
            'right': True,
            'bottom': True,
            'left': True
        }


class Maze:
    """Represent the maze structure and generation logic."""

    def __init__(self, width: int, height: int) -> None:
        """Initialize the maze grid with given dimensions."""
        self.width = width
        self.height = height
        self.grid = [
            [Cell(x, y) for y in range(height)]
            for x in range(width)
        ]

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """Return the cell at given coordinates or None if out of bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        return None

    def get_unvisited_neighbors(self, cell: Cell) -> List[Cell]:
        """Find and return unvisited adjacent cells."""
        neighbors = []
        top = self.get_cell(cell.x, cell.y - 1)
        if top and not top.visited:
            neighbors.append(top)
        right = self.get_cell(cell.x + 1, cell.y)
        if right and not right.visited:
            neighbors.append(right)
        bottom = self.get_cell(cell.x, cell.y + 1)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        left = self.get_cell(cell.x - 1, cell.y)
        if left and not left.visited:
            neighbors.append(left)
        return neighbors

    def remove_walls(self, current: Cell, next_cell: Cell) -> None:
        """Remove the wall between the current cell and the next cell."""
        dx = current.x - next_cell.x
        dy = current.y - next_cell.y
        if dx == 1:
            current.walls['left'] = False
            next_cell.walls['right'] = False
        elif dx == -1:
            current.walls['right'] = False
            next_cell.walls['left'] = False
        elif dy == 1:
            current.walls['top'] = False
            next_cell.walls['bottom'] = False
        elif dy == -1:
            current.walls['bottom'] = False
            next_cell.walls['top'] = False

    def generate(self) -> None:
        """Generate the maze using a randomized depth-first search."""
        start_cell = self.get_cell(0, 0)
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

    def display(self) -> None:
        """Print the maze in ASCII format to the console."""
        print("+" + "---+" * self.width)
        for y in range(self.height):
            row_str = "|"
            for x in range(self.width):
                cell = self.grid[x][y]
                row_str += "   "
                row_str += "|" if cell.walls['right'] else " "
            print(row_str)
            row_str = "+"
            for x in range(self.width):
                cell = self.grid[x][y]
                row_str += "---+" if cell.walls['bottom'] else "   +"
            print(row_str)


def load_config(filename: str) -> Tuple[int, int]:
    """Read and extract width and height integers from a config file."""
    try:
        with open(filename, 'r') as f:
            content = f.read()
            numbers = [int(num) for num in re.findall(r'\d+', content)]
            if len(numbers) >= 2:
                return numbers[0], numbers[1]
            print(
                "Erreur : Le fichier config.txt doit contenir "
                "au moins deux nombres."
            )
            sys.exit(1)
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{filename}' est introuvable.")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Utilisation : python3 maze_generator.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]
    width, height = load_config(config_file)
    print(f"Génération d'un labyrinthe de {width}x{height}...\n")

    mon_labyrinthe = Maze(width, height)
    mon_labyrinthe.generate()
    mon_labyrinthe.display()
