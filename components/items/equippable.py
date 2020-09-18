"""This file contains the implementation of the basic
equipment class and its immediate descendants.
"""

from .item import Item
from ..utilities.constants import colours as C


class Equippable(Item):
    """An equippable item."""

    def __init__(self, name, description, x, y,
                 char="/", colour=C["TEMP"]):
        super().__init__(name, description, x, y,
                         char, colour)
        self.equipped = False


class Weapon(Equippable):
    """An equippable weapon."""

    def __init__(self, name, description, x, y,
                 char="/", colour=C["TEMP"]):
        super().__init__(name, description, x, y,
                         char, colour)


class Armour(Equippable):
    """An equippable clothing item."""

    def __init__(self, name, description, x, y,
                 char="/", colour=C["TEMP"]):
        super().__init__(name, description, x, y,
                         char, colour)
