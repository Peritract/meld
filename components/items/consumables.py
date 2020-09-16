"""This file contains the implementations of the various
consumable items.
"""

from .consumable import Consumable
from ..utilities.constants import colours as C


class Bandage(Consumable):
    """A one-use healing item."""

    def __init__(self, x, y):
        super().__init__("bandage", 1, x, y, char="+", colour=C["RED"])
        self.power = 3

    def affect(self, target):
        """Heals the target."""
        target.body.heal(self.power)
