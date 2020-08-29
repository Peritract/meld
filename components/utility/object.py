"""
    This file contains the implementation of the basic
    "Object" class - any thing that exists in the game
    world.
"""

import tcod
from .position import Position


class Object:

    # Basic shared setup
    name = "thing"
    character = "%"
    colour = tcod.magenta
    blocks = True

    def __init__(self, position=Position(0, 0)):
        """Sets key properties"""
        self.position = position