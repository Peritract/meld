"""This file contains the implementation of the Consumable base class.
This is a limited-use item that is destroyed on use.
"""

from .item import Item
from ..utilities.constants import colours as C


class Consumable(Item):
    """An item that is consumed on use."""

    def __init__(self, name, description, uses, x, y,
                 char="!", colour=C["TEMP"]):
        super().__init__(name, description, x, y, char, colour)
        self.uses = uses

    @property
    def description_text(self):
        uses = f"{self.uses} uses" if self.uses > 1 else "1 use"
        return self.description + f" {uses} remaining."

    def use(self, target):
        """Uses the item"""
        if self.uses > 0:
            self.affect(target)
            self.uses -= 1

    def affect(self, target):
        """Applies the item's effect to the target."""
        raise NotImplementedError()
