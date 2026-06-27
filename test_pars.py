#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   test_pars.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bramahef <bramahef@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/09 11:19:53 by bramahef            #+#    #+#            #
#   Updated: 2026/06/27 16:35:13 by bramahef           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
from typing import Dict, Any, Tuple


def is_in_42_pattern(x: int, y: int, width: int, height: int) -> bool:
    """Check if coordinates are within the reserved 42 pattern area."""
    center_x = width // 2
    center_y = height // 2

    wall_42 = {
        (-3, -2), (-3, -1), (-3, 0), (-2, 0), (-1, -2), (-1, -1),
        (-1, 0), (-1, 1), (-1, 2),
        (1, -2), (2, -2), (3, -2), (3, -1),
        (1, 0), (2, 0), (3, 0), (1, 1), (1, 2), (2, 2), (3, 2)
    }

    dx = x - center_x
    dy = y - center_y
    return (dx, dy) in wall_42


def find_default_coord(width: int, height: int, exclude: Tuple[int, int]) -> Tuple[int, int]:
    """Find a valid default coordinate outside the 42 pattern."""
    # Try corners and edges first, excluding the provided coordinate
    candidates = [
        (0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1),
        (1, 0), (width - 2, 0), (0, 1), (0, height - 2),
        (width - 1, 1), (width - 1, height - 2), (1, height - 1), (width - 2, height - 1)
    ]

    for coord in candidates:
        if coord != exclude and not is_in_42_pattern(coord[0], coord[1], width, height):
            return coord

    # Fallback: find any valid coordinate
    for x in range(width):
        for y in range(height):
            if (x, y) != exclude and not is_in_42_pattern(x, y, width, height):
                return (x, y)

    # Should not reach here if maze is large enough
    return (0, 0)


def config_parser(filename: str) -> Dict[str, Any]:
    config: Dict[str, Any] = {}

    try:
        with open(filename, "r") as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    print(f"Erreur ligne {line_num}: pas de '='.")
                    sys.exit(1)

                key, value = line.split("=", 1)
                key = key.strip().lower()
                value = value.strip()

                if key in config:
                    print(f"Clé '{key}' déjà définie.")
                    sys.exit(1)

                try:
                    if key in ["width", "height"]:
                        config[key] = int(value)
                        if config[key] <= 0:
                            raise ValueError(f"{key} doit être supérieur à 0")

                    elif key in ["entry", "exit"]:
                        parts = value.split(",")

                        if len(parts) != 2:
                            raise ValueError("format attendu: x,y")

                        x, y = map(int, parts)
                        if x < 0 or y < 0:
                            raise ValueError(f"{key} ne peut pas etre négatif")
                        config[key] = (x, y)

                    elif key == "perfect":
                        if value == "True":
                            config[key] = True
                        elif value == "False":
                            config[key] = False
                        else:
                            raise ValueError("PERFECT doit être True ou False")

                    else:
                        config[key] = value

                except ValueError as e:
                    print(f"Erreur ligne {line_num}: {e}")
                    sys.exit(1)

    except FileNotFoundError:
        print(f"Erreur: le fichier '{filename}' est introuvable.")
        sys.exit(1)

    except PermissionError:
        print(f"Erreur: droits insuffisants pour lire '{filename}'.")
        sys.exit(1)

    mandt_keys = ["width", "height", "entry", "exit", "perfect", "output_file"]

    missing = [key for key in mandt_keys if key not in config]

    if missing:
        print("Erreur de configuration: clés manquantes : " + ", ".join(missing))
        sys.exit(1)

    width = config["width"]
    height = config["height"]
    entry_x, entry_y = config["entry"]
    exit_x, exit_y = config["exit"]

    if not (0 <= entry_x < width and 0 <= entry_y < height):
        print(
            f"Erreur d'interface: entry {config['entry']} est"
            f" hors des limites (Taille: {width}x{height})."
        )
        sys.exit(1)

    if not (0 <= exit_x < width and 0 <= exit_y < height):
        print(
            f"Erreur d'interface: exit {config['exit']} est"
            f" hors des limites (Taille: {width}x{height})."
        )
        sys.exit(1)

    if config["entry"] == config["exit"]:
        print(
            "Erreur d'interface: entry et exit doivent être"
            " à des coordonnées différentes."
        )
        sys.exit(1)

    # Check if entry or exit are in 42 pattern and apply defaults
    if is_in_42_pattern(entry_x, entry_y, width, height):
        print(f"Erreur: entry {config['entry']} est dans le motif '42' réservé.")
        sys.exit(1)

    if is_in_42_pattern(exit_x, exit_y, width, height):
        print(f"Erreur: exit {config['exit']} est dans le motif '42' réservé.")
        default_exit = find_default_coord(width, height, (entry_x, entry_y))
        print(f"Utilisation de exit par défaut: {default_exit}")
        config["exit"] = default_exit
        exit_x, exit_y = default_exit

    if width < 12 or height < 12:
        print(
            "Attention: La taille du labyrinthe est "
            "trop petite pour afficher le motif '42'."
        )
    return config


if __name__ == "__main__":
    # Récupère le fichier passé en argument comme demandé par le sujet
    if len(sys.argv) != 2:
        print("Usage: python3 test_pars.py config.txt")
        sys.exit(1)

    parsed_config = config_parser(sys.argv[1])
    print("Configuration chargée avec succès :", parsed_config)
