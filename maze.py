#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   maze.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: loandria <loandria@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/09 16:37:00 by bramahef            #+#    #+#            #
#   Updated: 2026/06/16 08:44:47 by loandria           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # On crée une grille (liste de listes) remplie de 15 (tous les murs fermés)
        self.grid = [[15 for _ in range(width)] for _ in range(height)]

    def render_ascii(self) -> None:
        """Génère un affichage visuel textuel de la grille actuelle."""
        for y in range(self.height):
            # 1. Dessiner les plafonds (Murs Nord)
            top_row = ""
            for x in range(self.width):
                # Si le bit 1 (Nord) est actif, on met un mur, sinon un espace
                top_row += "+---" if (self.grid[y][x] & 1) else "+   "
            print(top_row + "+")

            # 2. Dessiner les murs latéraux (Murs Ouest / Est)
            mid_row = ""
            for x in range(self.width):
                # Si le bit 8 (Ouest) est actif, on met une barre vertical
                mid_row += "|" if (self.grid[y][x] & 8) else " "
                mid_row += "   " # Espace intérieur de la case
            # Clôture du mur Est de la dernière case
            print(mid_row + "|")

        # Dessiner le sol tout en bas du labyrinthe
        print("+---" * self.width + "+")
