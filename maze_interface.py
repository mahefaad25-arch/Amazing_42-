#!/usr/bin/env python3

"""Interface module for graphical maze interaction."""
import signal
import time

from mazegen.maze import Cell
from mlx import Mlx
from mazegen import Maze, MazeGenerator
from maze_exporter import write_maze_file
from maze_solver import MazeSolver

CELL_SIZE = 20
ENTRY_COLOR = 0xFF0000FF
EXIT_COLOR = 0xFFFF0000
CENTER_42_COLOR = 0xFFFF5F00
COLOR_PALETTES = {
    1: {"wall": 0xFFFFFFFF, "path": 0xFF00FF00, "bg": 0x00000000},
    2: {"wall": 0xFF00FFFF, "path": 0xFFFF00FF, "bg": 0x00112233},
    3: {"wall": 0xFFFFCC00, "path": 0xFFFF3333, "bg": 0x001A1A1A},
}


def display_menu_instructions() -> None:
    """Display keyboard mappings to console on startup."""
    print(
        "\n=============================================\n"
        "        GRAPHICAL INTERFACE ACTIVE             \n"
        "===============================================\n"
        " Use your keyboard on the window:              \n"
        "  [1] -> Regenerate a new maze                 \n"
        "  [2] -> Show/Hide solution path               \n"
        "  [3] -> Rotate maze colors                    \n"
        "  [4] -> Quit                                  \n"
        "===============================================\n"
    )


class MazeViewer:
    """Manages interactive graphical maze display via MiniLibX."""

    def __init__(
            self,
            maze: Maze,
            start_coords: tuple[int, int],
            end_coords: tuple[int, int],
            output_file: str,
            path: list[Cell] | None = None,
            perfect: bool = True
    ) -> None:
        """Initialize the viewer with maze rendering state and controls.

        Args:
            maze: The Maze object to display.
            start_coords: Starting cell coordinates.
            end_coords: Ending cell coordinates.
            output_file: Filename where maze output is written.
            path: Optional ordered list of cells representing the solution.
            perfect: Whether the current maze is perfect or may contain loops.
        """
        self.maze = maze
        self.start_coords = start_coords
        self.end_coords = end_coords
        self.path = path if path else []
        self.show_path = True
        self.path_visible = True
        self.color_mode = 1
        self.perfect = perfect
        self.output_file = output_file
        self.animation_interval = 0.5
        self.last_animation = time.time()

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

    def draw_line(
            self,
            x1: int,
            y1: int,
            x2: int,
            y2: int,
            color: int
    ) -> None:
        """Draw a horizontal or vertical line on the window.

        Args:
            x1: Start x coordinate.
            y1: Start y coordinate.
            x2: End x coordinate.
            y2: End y coordinate.
            color: Pixel color value.
        """
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x1, y, color)
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y1, color)

    def draw_cell_background(self, cell: Cell, color: int) -> None:
        """Fill the interior of a cell with a solid background color.

        Args:
            cell: The cell to fill.
            color: The fill color value.
        """
        px = cell.x * CELL_SIZE
        py = cell.y * CELL_SIZE
        for x in range(px + 1, px + CELL_SIZE):
            for y in range(py + 1, py + CELL_SIZE):
                self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, color)

    def draw_cell_path(self, cell: Cell, color: int) -> None:
        """Draw a smaller colored block inside a cell for the solution path.

        Args:
            cell: The cell belonging to the path.
            color: The path highlight color.
        """
        px = cell.x * CELL_SIZE
        py = cell.y * CELL_SIZE
        for x in range(px + 7, px + CELL_SIZE - 7):
            for y in range(py + 7, py + CELL_SIZE - 7):
                self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, color)

    def render(self) -> None:
        """Render the maze, entry/exit markers, walls, and optional path.

        This method redraws the full window contents based on the current maze
        state, color mode, and path visibility settings.
        """
        self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        palette = COLOR_PALETTES[self.color_mode]

        for x in range(self.maze.width):
            for y in range(self.maze.height):
                cell = self.maze.get_cell(x, y)
                if cell:
                    color = CENTER_42_COLOR if cell.is_center_42 \
                        else palette["bg"]
                    self.draw_cell_background(cell, color)

        start_cell = self.maze.get_cell(*self.start_coords)
        end_cell = self.maze.get_cell(*self.end_coords)
        if start_cell:
            self.draw_cell_background(start_cell, ENTRY_COLOR)
        if end_cell:
            self.draw_cell_background(end_cell, EXIT_COLOR)

        if self.show_path and self.path_visible:
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

    def on_key(self, keycode: int, data: object) -> None:
        """Handle keypress events from the MiniLibX window.

        Args:
            keycode: The numeric code of the pressed key.
            data: Additional event data (unused).
        """
        if keycode == 49:
            print("[Menu] 1. Regenerating and reloading window...")
            self.maze = Maze(self.maze.width, self.maze.height)
            generator = MazeGenerator(self.maze, perfect=self.perfect)
            generator.generate(start_coords=self.start_coords)
            solver = MazeSolver(self.maze)
            self.path = solver.solve(
                start_coords=self.start_coords, end_coords=self.end_coords

            )
            write_maze_file(
                maze=self.maze,
                entry_coords=self.start_coords,
                exit_coords=self.end_coords,
                solution=self.path,
                filename=self.output_file,
            )
            self.render()
        elif keycode == 50:
            self.show_path = not self.show_path
            status = "DISPLAYED" if self.show_path else "HIDDEN"
            print(f"[Menu] 2. Solution path: {status}")
            self.render()
        elif keycode == 51:
            self.color_mode = (self.color_mode % 3) + 1
            print(f"[Menu] 3. Color rotation. Mode: {self.color_mode}")
            self.render()
        elif keycode == 52:
            print("[Menu] 4. Closing MiniLibX.")
            self.m.mlx_loop_exit(self.mlx_ptr)

    def _animation_tick(self, data: object) -> None:
        """Toggle the path animation state periodically.

        Args:
            data: Extra event data from the loop hook (unused).
        """
        now = time.time()
        if now - self.last_animation >= self.animation_interval:
            self.last_animation = now
            self.path_visible = not self.path_visible
            self.render()

    def _handle_sigint(self, signum: int, frame: object) -> None:
        """Custom SIGINT handler to exit the MiniLibX loop cleanly."""
        print("\nSIGINT received. Exiting MiniLibX loop...")
        self.m.mlx_loop_exit(self.mlx_ptr)

    def on_close(self, data: object) -> None:
        """Handle window close events by terminating the event loop.

        Args:
            data: Extra event data from the close event (unused).
        """
        self.m.mlx_loop_exit(self.mlx_ptr)

    def run(self) -> None:
        """Start the MiniLibX event loop and render the initial maze."""
        self.render()
        self.m.mlx_key_hook(self.win_ptr, self.on_key, None)
        self.m.mlx_hook(self.win_ptr, 33, 0, self.on_close, None)
        self.m.mlx_loop_hook(self.mlx_ptr, self._animation_tick, None)
        old_handler = signal.signal(signal.SIGINT, self._handle_sigint)
        try:
            self.m.mlx_loop(self.mlx_ptr)
        finally:
            signal.signal(signal.SIGINT, old_handler)
