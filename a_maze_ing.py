#!/usr/bin/env python3


import sys
from mazegen import Maze, MazeGenerator
from config_parser import config_parser
from maze_exporter import write_maze_file
from maze_solver import MazeSolver
try:
    from maze_interface import display_menu_instructions, MazeViewer
except Exception as e:
    print(e)
    sys.exit(1)

sys.setrecursionlimit(10000)


def main() -> None:
    """Parse configuration, generate the maze, solve it, and launch the viewer.

    This function reads the provided configuration file, creates the maze,
    generates passages, solves the maze, writes the maze output file, and
    launches the graphical viewer.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]
    config = config_parser(config_file)

    width = config["width"]
    height = config["height"]
    entry_x, entry_y = config["entry"]
    exit_x, exit_y = config["exit"]
    perfect = config["perfect"]
    seed = config["seed"]
    output_file = config["output_file"]

    start_coords = (entry_x, entry_y)
    end_coords = (exit_x, exit_y)
    maze = Maze(width, height)
    try:
        generator = MazeGenerator(maze, seed=seed, perfect=perfect)
        generator.generate(start_coords=start_coords)
    except KeyboardInterrupt:
        print("Maze generation interrupted by user.")
        sys.exit(1)

    solver = MazeSolver(maze)
    solution_path = solver.solve(
        start_coords=start_coords, end_coords=end_coords
    )

    write_maze_file(
        maze=maze,
        entry_coords=start_coords,
        exit_coords=end_coords,
        solution=solution_path,
        filename=output_file,
    )
    print(f"Maze written to '{output_file}'")

    display_menu_instructions()
    viewer = MazeViewer(
        maze,
        start_coords=start_coords,
        end_coords=end_coords,
        path=solution_path,
        perfect=perfect,
        output_file=output_file,
    )
    viewer.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
