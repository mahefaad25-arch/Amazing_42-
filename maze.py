# import re
# import sys
# from typing import List, Optional, Tuple


# class Cell:
#     """Represent a single cell in the maze grid with its walls."""

#     def __init__(self, x: int, y: int) -> None:
#         """Initialize the cell with coordinates and default active walls."""
#         self.x = x
#         self.y = y
#         self.visited = False
#         self.walls = {
#             'top': True,
#             'right': True,
#             'bottom': True,
#             'left': True
#         }


# class Maze:
#     """Manage the maze structure, including grid data and rendering."""

#     def __init__(self, width: int, height: int) -> None:
#         """Create the grid structure based on the provided dimensions."""
#         self.width = width
#         self.height = height
#         self.grid = [
#             [Cell(x, y) for y in range(height)]
#             for x in range(width)
#         ]

#     def get_cell(self, x: int, y: int) -> Optional[Cell]:
#         """Return the cell at coordinates (x, y) or None if out of bounds."""
#         if 0 <= x < self.width and 0 <= y < self.height:
#             return self.grid[x][y]
#         return None

#     def display(self, path: Optional[List[Cell]] = None) -> None:
#         """Output the grid and the optional solution path to the console."""
#         path_set = set(path) if path else set()

#         print("+" + "---+" * self.width)
#         for y in range(self.height):
#             row_str = "|"
#             for x in range(self.width):
#                 cell = self.grid[x][y]
#                 if cell in path_set:
#                     row_str += " * "
#                 else:
#                     row_str += "   "
#                 row_str += "|" if cell.walls['right'] else " "
#             print(row_str)

#             row_str = "+"
#             for x in range(self.width):
#                 cell = self.grid[x][y]
#                 row_str += "---+" if cell.walls['bottom'] else "   +"
#             print(row_str)


# def load_config(filename: str) -> Tuple[int, int]:
#     """Parse and return dimensions from the configuration file."""
#     try:
#         with open(filename, 'r') as f:
#             content = f.read()
#             numbers = [int(num) for num in re.findall(r'\d+', content)]
#             if len(numbers) >= 2:
#                 return numbers[0], numbers[1]
#             print("Erreur : Le fichier config.txt ", end="")
#             print("doit contenir au moins deux nombres.")
#             sys.exit(1)
#     except FileNotFoundError:
#         print(f"Erreur : Le fichier '{filename}' est introuvable.")
#         sys.exit(1)

# # maze.py
import re
import sys
from typing import List, Optional, Tuple


class Cell:
    """Represent a single cell in the maze grid with its walls."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize the cell with coordinates and default active walls."""
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
    """Manage the maze structure, including grid data and rendering."""

    def __init__(self, width: int, height: int) -> None:
        """Create the grid structure based on the provided dimensions."""
        self.width = width
        self.height = height
        self.grid = [
            [Cell(x, y) for y in range(height)]
            for x in range(width)
        ]

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """Return the cell at coordinates (x, y) or None if out of bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        return None

    def display(self, path: Optional[List[Cell]] = None) -> None:
        """Render the maze using solid high-contrast black and white blocks."""
        path_set = set(path) if path else set()
        r_width = self.width * 2 + 1
        r_height = self.height * 2 + 1

        grid = [["█" for _ in range(r_width)] for _ in range(r_height)]

        for x in range(self.width):
            for y in range(self.height):
                cell = self.grid[x][y]
                cx, cy = x * 2 + 1, y * 2 + 1

                grid[cy][cx] = "·" if cell in path_set else " "

                if not cell.walls['top'] and y > 0:
                    top_cell = self.grid[x][y - 1]
                    is_path = cell in path_set and top_cell in path_set
                    grid[cy - 1][cx] = "·" if is_path else " "

                if not cell.walls['bottom'] and y < self.height - 1:
                    bot_cell = self.grid[x][y + 1]
                    is_path = cell in path_set and bot_cell in path_set
                    grid[cy + 1][cx] = "·" if is_path else " "

                if not cell.walls['left'] and x > 0:
                    left_cell = self.grid[x - 1][y]
                    is_path = cell in path_set and left_cell in path_set
                    grid[cy][cx - 1] = "·" if is_path else " "

                if not cell.walls['right'] and x < self.width - 1:
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


def load_config(filename: str) -> Tuple[int, int]:
    """Parse and return dimensions from the configuration file."""
    try:
        with open(filename, 'r') as f:
            content = f.read()
            numbers = [int(num) for num in re.findall(r'\d+', content)]
            if len(numbers) >= 2:
                return numbers[0], numbers[1]
            print("Erreur : Le fichier config.txt ", end="")
            print("doit contenir au moins deux nombres.")
            sys.exit(1)
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{filename}' est introuvable.")
        sys.exit(1)
