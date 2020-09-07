"""
This file contains the implementation of the basic
"Object" class - any thing that exists in the game
world.
"""

import tcod


class Object:

    def __init__(self,
                 name="thing",
                 x=0,
                 y=0,
                 char="%",
                 colour=tcod.magenta,
                 blocks=True):

        """Sets key properties"""
        self.name = name
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.blocks = blocks
