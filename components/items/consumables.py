"""This file contains the implementations of the various
consumable items.
"""

from .consumable import Consumable
from ..utilities.constants import colours as C
from ..utilities.exceptions import Impossible


class Bandage(Consumable):
    """A one-use healing item."""

    def __init__(self, x, y):
        super().__init__("Bandage",
                         "A tattered scrap of cloth to bind a wound.",
                         1, x, y, char="+", colour=C["RED"])
        self.power = 3

    def affect(self, target):
        """Heals the target."""
        if target.body.health < target.body.max_health:
            target.body.heal(self.power)
        else:
            raise Impossible("You are already at full health.")
