#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   maze.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bramahef <bramahef@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/09 16:37:00 by bramahef            #+#    #+#            #
#   Updated: 2026/06/22 21:23:10 by bramahef           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # On crée une grille (liste de listes) remplie de 15 (tous les murs fermés)
        self.grid = [[15 for _ in range(width)] for _ in range(height)]

    def generate(self, start_x: int = 0, start_y: int = 0) -> None:
        """Génère le labyrinthe en place en utilisant DFS récursif itératif.

        La représentation utilise des bits pour les murs:
        Nord=1, Est=2, Sud=4, Ouest=8. Un bit à 1 signifie la présence d'un mur.
        Après la génération, les murs retirés auront leurs bits mis à 0.
        """
        import random

        # Bits pour les directions
        N, E, S, W = 1, 2, 4, 8
        dx = {N: 0, E: 1, S: 0, W: -1}
        dy = {N: -1, E: 0, S: 1, W: 0}
        opposite = {N: S, E: W, S: N, W: E}

        # Réinitialiser la grille (tous murs fermés)
        self.grid = [[15 for _ in range(self.width)] for _ in range(self.height)]
        visited = [[False for _ in range(self.width)] for _ in range(self.height)]

        # Pile pour DFS
        stack = [(start_x, start_y)]
        visited[start_y][start_x] = True

        while stack:
            x, y = stack[-1]

            # trouver voisins non visités
            neighbors = []
            # Nord
            if y - 1 >= 0 and not visited[y - 1][x]:
                neighbors.append((x, y - 1, N))
            # Est
            if x + 1 < self.width and not visited[y][x + 1]:
                neighbors.append((x + 1, y, E))
            # Sud
            if y + 1 < self.height and not visited[y + 1][x]:
                neighbors.append((x, y + 1, S))
            # Ouest
            if x - 1 >= 0 and not visited[y][x - 1]:
                neighbors.append((x - 1, y, W))

            if neighbors:
                nx, ny, direction = random.choice(neighbors)

                # retirer les murs entre (x,y) et (nx,ny)
                self.grid[y][x] &= ~direction
                self.grid[ny][nx] &= ~opposite[direction]

                visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()

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
