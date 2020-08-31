"""
This file contains the implementation of the LevelMap
class - this stores the map for a single in-game area.
"""

import numpy as np
from .tiles import unknown, basic_floor, basic_wall
from ..entities.entity import Entity
from tcod.map import compute_fov
from math import sqrt

import tcod

class Level:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Create a map of floor tiles, with x and y humanised.
        self.tiles = np.full((width, height),
                             fill_value=basic_floor,
                             order="F")

        # holders for details of visible/known tiles
        self.visible_tiles = np.full((width, height),
                                     fill_value=False,
                                     order="F")
        self.explored_tiles = np.full((width, height),
                                      fill_value=False,
                                      order="F")

        # Trash wall, for the exampling
        self.tiles[30:33, 22] = basic_wall

        # Trash entities, for the exampling
        self.entities = [Entity("Chett"),
                         Entity("Victoria", (1, 1)),
                         Entity("Velma", (2, 2))]

    # Utility functions - mostly about checking tiles for particular purposes

    def in_bounds(self, x, y):
        """Checks if a given point is inside the map bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_passable(self, x, y):
        """Checks if a tile in a given location is passable."""
        if self.tiles["passable"][x, y]:
            return True
        return False

    def distance_to(a, b):
        """Returns the distance between one point and another"""
        x_dist = a.x - b.x
        y_dist = a.y - b.y
        return sqrt(x_dist ** 2 + y_dist ** 2)

    # Rendering and FoV methods

    def update_fov(self, center):
        """Updates the visible area."""
        self.visible_tiles[:] = compute_fov(
            self.tiles["transparent"],
            (center.x, center.y),
            radius=center.view_radius,
            algorithm=tcod.FOV_SHADOW)

        # Mark all visible tiles as explored
        # Set explored to equal explored | visible (preserve any Trues in
        # either)
        self.explored_tiles |= self.visible_tiles

    def render(self, console, player):
        """Displays the game world on a given console."""

        # Update the current field of view
        # Centered on a specific entity
        self.update_fov(player)

        # Fill the map with tiles, choosing the correct appearance for each one
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible_tiles, self.explored_tiles],
            choicelist=[self.tiles["in_view"], self.tiles["out_of_view"]],
            default=unknown)

        # Display each entity
        for entity in self.entities:

            # If it's in view
            if self.visible_tiles[entity.x, entity.y]:
                console.print(entity.x,
                              entity.y,
                              entity.character,
                              entity.colour)

    # Entity management

    def handle_actions(self):
        """Allow each entity to act."""
        for entity in self.entities:
            entity.take_action(self)
