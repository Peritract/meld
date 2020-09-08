"""
This file contains the implementation of the base Area class.
This is a single in-game location.
"""

from ..entities.entity import Entity


class Area:
    """An in-game location."""

    def __init__(self, width, height, world, name="area"):
        self.width = width
        self.height = height
        self.world = world
        self.name = name

        # Holders for all internal objects
        self.contents = set()

    @property
    def entities(self):
        """Returns a set of entities in the area."""
        return set([thing for thing in self.contents
                    if isinstance(thing, Entity)])

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
