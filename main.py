#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   main.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bramahef <bramahef@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/23 07:42:31 by loandria            #+#    #+#            #
#   Updated: 2026/06/26 09:23:14 by bramahef           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
from maze import Maze
from test_pars import config_parser
from maze_exporter import write_maze_file
from maze_generator import MazeGenerator
from solver import MazeSolver


def main() -> None:
    """Orchestrate maze creation, generation, and solving processes."""
    if len(sys.argv) < 2:
        print("Utilisation : python3 main.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]

    # Utilisation de ton vrai parser de test_pars.py
    config = config_parser(config_file)

    width = config["width"]
    height = config["height"]

    entry_x, entry_y = config["entry"]
    exit_x, exit_y = config["exit"]

    start_coords = (entry_x, entry_y)
    end_coords = (exit_x, exit_y)

    # Initialisation de la structure
    maze = Maze(width, height)

    # Génération du labyrinthe à partir de l'entrée officielle
    generator = MazeGenerator(maze)
    generator.generate(start_coords=start_coords)

    # Résolution du labyrinthe de l'entrée vers la sortie officielle
    solver = MazeSolver(maze)
    chemin_solution = solver.solve(start_coords=start_coords, end_coords=end_coords)

    output_file = config["output_file"]
    write_maze_file(
        maze=maze,
        entry_coords=start_coords,
        exit_coords=end_coords,
        solution=chemin_solution,
        filename=output_file,
    )
    print(f"Maze written to '{output_file}'")

    if chemin_solution:
        maze.display(path=chemin_solution)
    else:
        print("Erreur : Aucun chemin de résolution trouvé.")


if __name__ == "__main__":
    main()
