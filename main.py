#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   main.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: loandria <loandria@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/23 07:42:31 by loandria            #+#    #+#            #
#   Updated: 2026/06/23 07:42:37 by loandria           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
from maze import Maze, load_config
from maze_generator import MazeGenerator
from maze_solver import MazeSolver


def main() -> None:
    """Orchestrate maze creation, generation, and solving processes."""
    if len(sys.argv) < 2:
        print("Utilisation : python3 main.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]
    width, height = load_config(config_file)

    maze = Maze(width, height)

    generator = MazeGenerator(maze)
    generator.generate()
    solver = MazeSolver(maze)
    chemin_solution = solver.solve()

    if chemin_solution:
        maze.display(path=chemin_solution)


if __name__ == "__main__":
    main()
