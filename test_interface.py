#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   test_interface.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: loandria <loandria@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/09 16:33:10 by bramahef            #+#    #+#            #
#   Updated: 2026/06/23 07:42:14 by loandria           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
from typing import Dict, Any
from maze import Maze
from test_pars import config_parser


def display_menu() -> str:
    """Affiche le menu d'interactions requis par le sujet."""
    print("\n=== A-Maze-ing ===")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate maze colors")
    print("4. Quit")
    return input("Choice? (1-4): ").strip()


def start_interface(config: Dict[str, Any]):
    show_path = False
    color_mode = 1

    # Instance de notre labyrinthe initialisé avec les tailles du parser
    mon_labyrinthe = Maze(config["width"], config["height"])
    print(f"\nInitialisation d'une grille de {config['width']}x{config['height']}...")

    while True:
        # 1. On affiche le rendu visuel ASCII à chaque tour de boucle
        mon_labyrinthe.render_ascii()
        print(f"[Mode visuel : Couleur={color_mode}, AfficherChemin={show_path}]")

        # 2. On récupère le choix utilisateur
        choice = display_menu()

        # 3. Gestion des choix
        if choice == "1":
            print("Régénération d'un nouveau labyrinthe (Aléatoire)...")
            # Plus tard : mon_labyrinthe.generate()
        elif choice == "2":
            show_path = not show_path
            print(f"Chemin de résolution : {'AFFICHÉ' if show_path else 'MASQUÉ'}")
        elif choice == "3":
            color_mode = (color_mode % 3) + 1
            print(f"Changement du mode couleur vers : {color_mode}")
        elif choice == "4":
            print("Fermeture propre du système. Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez entrer un nombre entre 1 et 4.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 test_interface.py config.txt")
        sys.exit(1)

    ma_config = config_parser(sys.argv[1])
    start_interface(ma_config)

"""

maze = [
    [_, _, _],
    [_, _, _],
    [_, _, _],
]



def find_neigboor(maze, x, y) -> list[Cell]:
    neighboor = []
    if not maze[x - 1][y].visited:
        neightboor.append(maze[x - 1][y])
    neightboor.append(maze[x + 1][y])
    neightboor.append(maze[x][y - 1])
    neightboor.append(maze[x][y + 1])
    return neightboor


def find_recursive(maze: list[list[Any]], x: int, y: int) -> None:
    maze[x][y].visited = True
    cell_neighboors = find_neighboor(maze, x, y) # rechercher les voisi de maze[x][y]
    cell_neighboors = random.shuffle(cell_neighboors) # randomiser les place des voisin
    for neighboor in cell_neighboors:
        break_wall(neighboor)
        break_wall(maze[x][y])
        find_recursive(maze, neightboor.x, neightboor.y)

"""
