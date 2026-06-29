#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   maze_animation.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: bramahef <bramahef@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/29 16:13:32 by bramahef            #+#    #+#            #
#   Updated: 2026/06/29 16:13:33 by bramahef           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


import time
from typing import List

from maze import Maze, Cell


def animate_path_progressive(
    maze: Maze,
    path: List[Cell],
    entry_coords: tuple[int, int],
    exit_coords: tuple[int, int],
    delay: float = 0.12,
) -> None:
    """Animate the maze solution from entry to exit, one point at a time."""
    if not path:
        return

    try:
        for index in range(1, len(path) + 1):
            print("\033[H\033[J", end="")
            maze.display(
                path[:index],
                entry_coords=entry_coords,
                exit_coords=exit_coords,
            )
            time.sleep(delay)
    except KeyboardInterrupt:
        pass
