"""
This class contains the implementation of the World class.
A World contains information about several levels and the
connections between them.
"""


class World:
    """Manages the in-game environments."""

    def __init__(self, engine=None, player=None):
        self.engine = engine

        self.player = player
        self.current_area = 0
        self.areas = []

    @property
    def area(self):
        """Returns the currently-occupied area."""
        return self.areas[self.current_area]

    @property
    def entities(self):
        """Returns the entities in the currently-occupied area."""
        return self.areas[self.current_area].entities
