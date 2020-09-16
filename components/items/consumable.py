"""This file contains the implementation of the Consumable base class.
This is a limited-use item that is destroyed on use.
"""

from .item import Item
from ..utilities.constants import colours as C


class Consumable(Item):
    """An item that is consumed on use."""

    def __init__(self, name, uses, x, y, char="!", colour=C["YELLOW"]):
        super().__init__(name, x, y, True, False, char, colour)
        self.uses = uses

    def use(self, target):
        """Uses the item"""
        if self.uses > 0:
            self.uses -= 1
            self.affect(target)

    def affect(self, target):
        """Applies the item's effect to the target."""
        raise NotImplementedError()
