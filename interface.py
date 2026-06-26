#!/usr/bin/env python3
"""Interface module for graphical maze interaction."""
from mlx import Mlx
from maze import Maze
from maze_generator import MazeGenerator
from solver import MazeSolver

CELL_SIZE = 20
ENTRY_COLOR = 0xFF0000FF  # Bleu pur pour l'entrée
EXIT_COLOR = 0xFFFF0000  # Rouge pur pour la sortie
COLOR_PALETTES = {
    1: {"wall": 0xFFFFFFFF, "path": 0xFF00FF00, "bg": 0x00000000},
    2: {"wall": 0xFF00FFFF, "path": 0xFFFF00FF, "bg": 0x00112233},
    3: {"wall": 0xFFFFCC00, "path": 0xFFFF3333, "bg": 0x001A1A1A},
}


def display_menu_instructions() -> None:
    """Affiche les correspondances clavier dans la console au lancement."""
    print(
        "\n=============================================\n"
        "        INTERFACE GRAPHIQUE ACTIVE           \n"
        "=============================================\n"
        " Utilisez votre clavier sur la fenêtre :     \n"
        "  [1] ou [R] -> Re-generate a new maze       \n"
        "  [2] ou [H] -> Show/Hide path from entry    \n"
        "  [3] ou [C] -> Rotate maze colors           \n"
        "  [4] ou [ECHAP] ou [Q] -> Quit              \n"
        "=============================================\n"
    )


class MazeViewer:
    """Gère l'affichage graphique interactif du labyrinthe via MiniLibX."""

    def __init__(self, maze: Maze, start_coords, end_coords, path=None):
        self.maze = maze
        self.start_coords = start_coords
        self.end_coords = end_coords
        self.path = path if path else []
        self.show_path = True
        self.color_mode = 1

        self.m = Mlx()
        self.mlx_ptr = self.m.mlx_init()
        self.win_width = maze.width * CELL_SIZE + 1
        self.win_height = maze.height * CELL_SIZE + 1
        self.win_ptr = self.m.mlx_new_window(
            self.mlx_ptr,
            self.win_width,
            self.win_height,
            "A-Maze-ing - MiniLibX Interface",
        )

    def draw_line(self, x1, y1, x2, y2, color):
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x1, y, color)
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y1, color)

    def draw_cell_background(self, cell, color):
        px = cell.x * CELL_SIZE
        py = cell.y * CELL_SIZE
        for x in range(px + 1, px + CELL_SIZE):
            for y in range(py + 1, py + CELL_SIZE):
                self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, color)

    def draw_cell_path(self, cell, color):
        px = cell.x * CELL_SIZE
        py = cell.y * CELL_SIZE
        for x in range(px + 7, px + CELL_SIZE - 7):
            for y in range(py + 7, py + CELL_SIZE - 7):
                self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, color)

    def render(self):
        self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        palette = COLOR_PALETTES[self.color_mode]

        for x in range(self.maze.width):
            for y in range(self.maze.height):
                cell = self.maze.get_cell(x, y)
                if cell:
                    self.draw_cell_background(cell, palette["bg"])

        start_cell = self.maze.get_cell(*self.start_coords)
        end_cell = self.maze.get_cell(*self.end_coords)
        if start_cell:
            self.draw_cell_background(start_cell, ENTRY_COLOR)
        if end_cell:
            self.draw_cell_background(end_cell, EXIT_COLOR)

        if self.show_path:
            for cell in self.path:
                if (cell.x, cell.y) != self.start_coords and (
                    cell.x,
                    cell.y,
                ) != self.end_coords:
                    self.draw_cell_path(cell, palette["path"])

        for x in range(self.maze.width):
            for y in range(self.maze.height):
                cell = self.maze.get_cell(x, y)
                if not cell:
                    continue
                px = x * CELL_SIZE
                py = y * CELL_SIZE
                if cell.walls["top"]:
                    self.draw_line(px, py, px + CELL_SIZE, py, palette["wall"])
                if cell.walls["right"]:
                    self.draw_line(
                        px + CELL_SIZE,
                        py,
                        px + CELL_SIZE,
                        py + CELL_SIZE,
                        palette["wall"],
                    )
                if cell.walls["bottom"]:
                    self.draw_line(
                        px,
                        py + CELL_SIZE,
                        px + CELL_SIZE,
                        py + CELL_SIZE,
                        palette["wall"],
                    )
                if cell.walls["left"]:
                    self.draw_line(px, py, px, py + CELL_SIZE, palette["wall"])

    def on_key(self, keycode, data):
        if keycode == 49 or keycode == 114:
            print("[Menu] 1. Re-génération et rechargement de la fenêtre...")
            self.maze = Maze(self.maze.width, self.maze.height)
            generator = MazeGenerator(self.maze)
            generator.generate(start_coords=self.start_coords)
            solver = MazeSolver(self.maze)
            self.path = solver.solve(
                start_coords=self.start_coords, end_coords=self.end_coords
            )
            self.render()
        elif keycode == 50 or keycode == 104:
            self.show_path = not self.show_path
            status = "AFFICHÉ" if self.show_path else "MASQUÉ"
            print(f"[Menu] 2. Chemin de résolution : {status}")
            self.render()
        elif keycode == 51 or keycode == 99:
            self.color_mode = (self.color_mode % 3) + 1
            print(f"[Menu] 3. Rotation des couleurs. Mode : {self.color_mode}")
            self.render()
        elif keycode in [52, 65307, 53, 113]:
            print("[Menu] 4. Fermeture de la MiniLibX.")
            self.m.mlx_loop_exit(self.mlx_ptr)

    def on_close(self, data):
        self.m.mlx_loop_exit(self.mlx_ptr)

    def run(self):
        self.render()
        self.m.mlx_key_hook(self.win_ptr, self.on_key, None)
        self.m.mlx_hook(self.win_ptr, 33, 0, self.on_close, None)
        self.m.mlx_loop(self.mlx_ptr)
