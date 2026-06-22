#!/usr/bin/env python3

from mlx import Mlx

try:
    from maze_generator import Maze as GenMaze
except Exception:
    GenMaze = None

from maze_generator import Maze



CELL_SIZE = 20
WALL_COLOR = 0xFFFFFFFF


class MazeViewer:
    def __init__(self, maze):
        self.maze = maze

        self.m = Mlx()
        self.mlx_ptr = self.m.mlx_init()

        self.win_width = maze.width * CELL_SIZE + 1
        self.win_height = maze.height * CELL_SIZE + 1

        self.win_ptr = self.m.mlx_new_window(
            self.mlx_ptr,
            self.win_width,
            self.win_height,
            "A-Maze-ing"
        )

    def draw_line(self, x1, y1, x2, y2, color):
        """zz
        Dessine une ligne horizontale ou verticale.
        """

        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1

            for y in range(y1, y2 + 1):
                self.m.mlx_pixel_put(
                    self.mlx_ptr,
                    self.win_ptr,
                    x1,
                    y,
                    color
                )

        elif y1 == y2:
            if x1 > x2:
                x1, x2 = x2, x1

            for x in range(x1, x2 + 1):
                self.m.mlx_pixel_put(
                    self.mlx_ptr,
                    self.win_ptr,
                    x,
                    y1,
                    color
                )

    def draw_maze(self):
        for y in range(self.maze.height):
            for x in range(self.maze.width):

                # Support two grid layouts:
                # - bit-grid: grid[y][x] is an int with bits for walls
                # - cell-grid: grid[x][y] is a Cell object with a 'walls' dict
                g = self.maze.grid
                try:
                    if len(g) == self.maze.height:
                        cell = g[y][x]
                    else:
                        cell = g[x][y]
                except Exception:
                    # fallback
                    cell = g[y][x]

                px = x * CELL_SIZE
                py = y * CELL_SIZE

                # Convert cell to bitmask if necessary
                if isinstance(cell, int):
                    bits = cell
                else:
                    # assume object with 'walls' mapping: top,right,bottom,left -> True means wall
                    walls = getattr(cell, 'walls', None)
                    if walls is None:
                        # try attribute names used elsewhere
                        walls = {}
                        for name in ('top', 'right', 'bottom', 'left'):
                            walls[name] = getattr(cell, name, False)
                    bits = 0
                    if walls.get('top', False):
                        bits |= 1
                    if walls.get('right', False):
                        bits |= 2
                    if walls.get('bottom', False):
                        bits |= 4
                    if walls.get('left', False):
                        bits |= 8

                # Nord
                if bits & 1:
                    self.draw_line(
                        px,
                        py,
                        px + CELL_SIZE,
                        py,
                        WALL_COLOR
                    )

                # Est
                if bits & 2:
                    self.draw_line(
                        px + CELL_SIZE,
                        py,
                        px + CELL_SIZE,
                        py + CELL_SIZE,
                        WALL_COLOR
                    )

                # Sud
                if bits & 4:
                    self.draw_line(
                        px,
                        py + CELL_SIZE,
                        px + CELL_SIZE,
                        py + CELL_SIZE,
                        WALL_COLOR
                    )

                # Ouest
                if bits & 8:
                    self.draw_line(
                        px,
                        py,
                        px,
                        py + CELL_SIZE,
                        WALL_COLOR
                    )

    def on_key(self, keycode, data):
        print("Key:", keycode)

        # ESC sous Linux/X11
        if keycode == 65307:
            self.m.mlx_loop_exit(self.mlx_ptr)

    def on_close(self, data):
        self.m.mlx_loop_exit(self.mlx_ptr)

    def run(self):
        self.draw_maze()

        self.m.mlx_key_hook(
            self.win_ptr,
            self.on_key,
            None
        )

        self.m.mlx_hook(
            self.win_ptr,
            33,
            0,
            self.on_close,
            None
        )

        self.m.mlx_loop(self.mlx_ptr)


def main():
    width = 20
    height = 20

    maze = Maze(width, height)

    maze.generate(20, 20)

    viewer = MazeViewer(maze)

    viewer.run()


if __name__ == "__main__":
    main()