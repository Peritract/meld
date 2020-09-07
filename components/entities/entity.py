"""
    This file contains the implementation of the base Entity class;
    An entity is any object more complex than a simple physical item.
"""

from ..utilities.object import Object
import tcod


class Entity(Object):
    """The base class for all animate game objects"""

    def __init__(self,
                 name="entity",
                 x=0,
                 y=0,
                 faction="neutral",
                 char="&",
                 colour=tcod.lime,
                 blocks=True):
        super().__init__(name, x, y, char, colour, blocks)
        self.faction = faction

    def take_action(self):
        """Acts in the game world."""
        print("Here!")
