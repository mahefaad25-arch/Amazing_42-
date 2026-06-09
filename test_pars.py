#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   test_pars.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bramahef <bramahef@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/09 11:19:53 by bramahef            #+#    #+#            #
#   Updated: 2026/06/09 16:38:20 by bramahef           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys
from typing import Dict, Any


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
                key = key.strip()
                value = value.strip()

                if key in config:
                    print(f"Clé '{key}' déjà définie.")
                    sys.exit(1)

                try:
                    if key in ["WIDTH", "HEIGHT"]:
                        config[key] = int(value)
                        if config[key] <= 0:
                            raise ValueError(f"{key} doit être supérieur à 0")

                    elif key in ["ENTRY", "EXIT"]:
                        parts = value.split(",")

                        if len(parts) != 2:
                            raise ValueError("format attendu: y,x")

                        y, x = map(int, parts)
                        if y < 0 or x < 0:
                            raise ValueError(f"{key} ne peut pas etre négatif")
                        config[key] = (y, x)

                    elif key == "PERFECT":
                        if value == "True":
                            config[key] = True
                        elif value == "False":
                            config[key] = False
                        else:
                            raise ValueError(
                                "PERFECT doit être True ou False"
                            )

                    else:
                        config[key] = value

                except ValueError as e:
                    print(f"Erreur ligne {line_num}: {e}")
                    sys.exit(1)

    except FileNotFoundError:
        print(f"Erreur: le fichier '{filename}' est introuvable.")
        sys.exit(1)

    except PermissionError:
        print(
            f"Erreur: droits insuffisants pour lire '{filename}'."
        )
        sys.exit(1)

    mandt_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "PERFECT", "OUTPUT_FILE"]

    missing = [key for key in mandt_keys if key not in config]

    if missing:
        print(
            "Erreur de configuration: clés manquantes : "
            + ", ".join(missing)
        )
        sys.exit(1)

    width = config["WIDTH"]
    height = config["HEIGHT"]
    entry_y, entry_x = config["ENTRY"]
    exit_y, exit_x = config["EXIT"]

    if not (0 <= entry_x < width and 0 <= entry_y < height):
        print(f"Erreur d'interface: ENTRY {config['ENTRY']} est"
              f" hors des limites (Taille: {width}x{height}).")
        sys.exit(1)

    if not (0 <= exit_x < width and 0 <= exit_y < height):
        print(f"Erreur d'interface: EXIT {config['EXIT']} est"
              f" hors des limites (Taille: {width}x{height}).")
        sys.exit(1)

    if config["ENTRY"] == config["EXIT"]:
        print(
            "Erreur d'interface: ENTRY et EXIT doivent être"
            " à des coordonnées différentes."
        )
        sys.exit(1)

    if width < 12 or height < 12:
        print(
            "Attention: La taille du labyrinthe est "
            "trop petite pour afficher le motif '42'."
        )
    return config


if __name__ == "__main__":
    # Récupère le fichier passé en argument comme demandé par le sujet
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.argv = [sys.argv[0], "config.txt"]
    parsed_config = config_parser(sys.argv[1])
    print("Configuration chargée avec succès :", parsed_config)
