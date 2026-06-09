#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   test_pars.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bramahef <bramahef@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/09 11:19:53 by bramahef            #+#    #+#            #
#   Updated: 2026/06/09 13:28:46 by bramahef           ###   ########.fr      #
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
                    print(f"Erreur dans la ligne {line_num}: Pas de '='.")
                    sys.exit(1)
                    
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                
                try:
                    # Conversion des types
                    if key in ["WIDTH", "HEIGHT"]:
                        config[key] = int(value)
                    elif key in ["ENTRY", "EXIT"]:
                        y, x = value.split(",")
                        config[key] = (int(y), int(x))
                    elif key == "PERFECT":
                        config[key] = (value == "True")
                    else:
                        # Permet de stocker d'autres clés optionnelles (seed, etc.)
                        config[key] = value
                except ValueError:
                    print(f"Erreur de valeur ligne {line_num}: Impossible de convertir '{value}' pour la clé '{key}'.")
                    sys.exit(1)
                    
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{filename}' est introuvable.")
        sys.exit(1)
    except PermissionError:
        print(f"Erreur: Droits insuffisants pour lire le fichier '{filename}'.")
        sys.exit(1)
        
    # Vérification des clés obligatoires requises par le sujet
    mandatory_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "PERFECT", "OUTPUT_FILE"]
    for m_key in mandatory_keys:
        if m_key not in config:
            print(f"Erreur de configuration: La clé obligatoire '{m_key}' est manquante.")
            sys.exit(1)
            
    return config

# Exemple d'utilisation sécurisé
if __name__ == "__main__":
    # Récupère le fichier passé en argument comme demandé par le sujet
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.argv = [sys.argv[0], "config.txt"] # Fallback automatique pour tes tests locaux
        
    parsed_config = config_parser(sys.argv[1])
    print("Configuration chargée avec succès :", parsed_config)