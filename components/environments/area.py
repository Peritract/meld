"""
This file contains the implementation of the base Area class.
This is a single in-game location.
"""

from ..entities.entity import Entity
from ..environments.tiles import basic_floor, unknown
import numpy as np
from tcod.map import compute_fov
import tcod


class Area:
    """An in-game location."""

    def __init__(self, width, height, world, name="area"):
        self.width = width
        self.height = height
        self.world = world
        self.name = name

        # Holders for all internal objects
        self.contents = set()

        # ---HACK--- #

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

        # ---/HACK--- #

    @property
    def entities(self):
        """Returns a set of entities in the area."""
        return set([thing for thing in self.contents
                    if isinstance(thing, Entity)])

    def is_visible(self, x, y):
        """Checks if a given point is visible."""
        return self.visible_tiles[x, y]

    def in_bounds(self, x, y):
        """Checks if a given point is inside the area bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def at_location(self, x, y):
        """Returns a set of objects at the given location."""
        if self.in_bounds(x, y):
            return set([thing for thing in self.contents
                        if thing.x == x and thing.y == y])

    def get_blocker_at_location(self, x, y):
        """Returns the blocking entity at a particular position."""

        # Get all objects on the tile
        present = self.at_location(x, y)

        for thing in present:
            if thing.blocks:
                return thing

    def calculate_fov(self, entity):
        """Returns the visible area for a particular entity"""

        # Get a map the size of the level
        visible = np.full((self.width, self.height),
                          fill_value=False,
                          order="F")

        # Compute field of view from the entity's location
        visible[:] = compute_fov(self.tiles["transparent"],
                                 (entity.x, entity.y),
                                 radius=entity.body.view_radius,
                                 algorithm=tcod.FOV_SHADOW)

        # Return the visible map
        return visible

    def get_tile_appearances(self):
        """Get the current appearance of each tile."""
        return np.select(condlist=[self.visible_tiles,
                                   self.explored_tiles],
                         choicelist=[self.tiles["in_view"],
                                     self.tiles["out_of_view"]],
                         default=unknown)

    def update_tile_states(self, entity):
        """Updates the state of tiles (visible/explored)
           based on a given entity."""

        # Update the visible tiles based on the player's FoV
        self.visible_tiles = self.calculate_fov(entity)

        # Update explored tiles based on the visible ones
        # Set explored to equal explored | visible (preserve any Trues in
        # either)
        self.explored_tiles |= self.visible_tiles

        # Utility functions

    def post_message(self, message):
        """Adds a message to the associated message log."""
        self.world.engine.message_log.add_message(message)
