"""This file contains the implementations of the various
consumable items.
"""

from .items import Consumable
from ..utilities.constants import COLOURS as C
from ..utilities.exceptions import Impossible


class Bandage(Consumable):
    """A one-use healing item."""

    def __init__(self, x, y, area=None):
        super().__init__("Bandage",
                         "A tattered scrap of cloth to bind a wound.",
                         1, x, y, "+", C["RED"], area)
        self.power = 3

    def affect(self, target):
        """Heals the target."""
        if target.body.health < target.body.max_health:
            target.body.heal(self.power)
        else:
            raise Impossible("You are already at full health.")


class AcidFlask(Consumable):
    """A container of strong acid."""

    def __init__(self, x, y, area=None):
        super().__init__("Acid flask",
                         "A stoppered flask of powerful acid.",
                         1, x, y, "!", C["GREEN"], area)
        self.impact_radius = 3

    def affect(self, target):
        """Burns the consumer's insides."""
        target.body.health -= 10

    def impact(self):
        """When thrown, splashes acid over the nearby area."""

        # Find all the tiles in range

        pass
