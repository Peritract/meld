"""
This file contains the implementation of the base Area class.
This is a single in-game location.
"""


class Area:
    """An in-game location."""

    def __init__(self, width, height, world):
        self.width = width
        self.height = height
        self.world = world

        # Holders for objects
        self.entities = []
        self.items = []