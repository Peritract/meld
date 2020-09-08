"""
    This file contains the implementation of the base Entity class;
    An entity is any object more complex than a simple physical item.
"""

from ..utilities.object import Object
from ..entities.body import Body
import tcod


class Entity(Object):
    """The base class for all animate game objects"""

    def __init__(self,
                 name="entity",
                 x=0,
                 y=0,
                 faction="neutral",
                 body=Body,
                 char="&",
                 colour=tcod.lime,
                 blocks=True):
        super().__init__(name, x, y, char, colour, blocks)
        self.faction = faction
        self.body = body()

    def take_action(self):
        """Acts in the game world."""
        print(f"the {self.name} ponders.")

    def move(self, dx, dy):
        """Alters the entity's position by a given amount."""
        self.x += dx
        self.y += dy

    def attack(self, other):
        """Attacks another entity."""
        print(f"The {self.name} savages the {other.name}.")
