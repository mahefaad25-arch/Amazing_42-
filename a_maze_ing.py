#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   a_maze_ing.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bramahef <bramahef@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/25 16:40:00 by bramahef            #+#    #+#            #
#   Updated: 2026/06/25 17:43:42 by bramahef           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys

# Augmente la limite de récursion à 10 000 au lieu de 1 000 au cas où
sys.setrecursionlimit(10000)

from maze import Maze
from test_pars import config_parser
from maze_generator import MazeGenerator
from solver import MazeSolver
from interface import display_menu_instructions, MazeViewer


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]
    config = config_parser(config_file)

    width = config["width"]
    height = config["height"]
    entry_y, entry_x = config["entry"]
    exit_y, exit_x = config["exit"]

    start_coords = (entry_x, entry_y)
    end_coords = (exit_x, exit_y)

    maze = Maze(width, height)
    generator = MazeGenerator(maze)
    generator.generate(start_coords=start_coords)

    solver = MazeSolver(maze)
    chemin_solution = solver.solve(start_coords=start_coords, end_coords=end_coords)

    display_menu_instructions()
    viewer = MazeViewer(
        maze, start_coords=start_coords, end_coords=end_coords, path=chemin_solution
    )
    viewer.run()


if __name__ == "__main__":
    main()
