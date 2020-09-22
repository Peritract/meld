"""
This file contains the implementation of the basic
"Object" class - any thing that exists in the game
world.
"""

from .constants import COLOURS as C


class Object:

    def __init__(self,
                 name="thing",
                 description="A nondescript object.",
                 x=0,
                 y=0,
                 char="%",
                 colour=C["TEMP"],
                 blocks=True,
                 area=None):

        """Sets key properties"""
        self.name = name
        self.description = description
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.blocks = blocks
        self.area = area

    @property
    def description_text(self):
        """Returns the description for display."""
        return self.description
