"""This file contains the implementation of the basic
equipment class.
"""

from .item import Item
from ..utilities.constants import colours as C


class Equippable(Item):
    """An equippable item."""

    def __init__(self, name, type, x, y, char, colour):
        super().__init__(name, x, y, False, True,
                         "/", colour=C["YELLOW"])
        self.type = type
        self.equipped = False
