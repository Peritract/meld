"""This file contains the various necessary constants for the game."""

import tcod

DIRECTIONS = {
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
    "UP": (0, -1),
    "DOWN": (0, 1)
}

COLOURS = {
    "RED": tcod.red,
    "WHITE": tcod.white,
    "GREY": tcod.grey,
    "YELLOW": tcod.yellow,
    "GOLD": tcod.gold,
    "BROWN": tcod.brass,
    "BLACK": tcod.black,
    "GREEN": tcod.green,
    "TEMP": tcod.chartreuse
}
