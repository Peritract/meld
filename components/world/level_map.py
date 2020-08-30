"""
This file contains the implementation of the LevelMap
class - this stores the map for a single in-game area.
"""

import numpy as np
from .tiles import basic_floor, basic_wall


class LevelMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Create a map of floor tiles, with x and y humanised.
        self.tiles = np.full((width, height),
                             fill_value=basic_floor,
                             order="F")

        # Trash wall, for the exampling
        self.tiles[30:33, 22] = basic_wall

    def in_bounds(self, x, y):
        """Checks if a given point is inside the map bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console):
        """Displays all the tiles on a given console."""
        console.tiles_rgb[0:self.width,
                          0:self.height] = self.tiles["out_of_view"]
