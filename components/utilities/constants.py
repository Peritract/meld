"""This file contains the various necessary constants for the game."""

import tcod

directions = {
    "left": (-1, 0),
    "right": (1, 0),
    "up": (0, -1),
    "down": (0, 1)
}

colours = {
    "RED": tcod.red,
    "WHITE": tcod.white,
    "GREY": tcod.grey,
    "YELLOW": tcod.yellow
}
