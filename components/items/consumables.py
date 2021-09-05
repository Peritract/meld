"""This file contains the implementations of the various
consumable items.
"""

from .items import Consumable
from ..utilities.constants import COLOURS as C
from ..utilities.exceptions import Impossible
from ..utilities.messages import CombatMessage, AlertMessage


class Bandage(Consumable):
    """A one-use healing item."""

    def __init__(self, x=0, y=0, area=None):
        super().__init__("Bandage",
                         "A tattered scrap of cloth to bind a wound.",
                         "use",
                         1, x, y, "+", C["RED"], area)
        self.health = 3

    def affect(self, target):
        """Heals the target."""
        if target.body.health < target.body.max_health:
            target.body.heal(self.health)
            if target.faction == 'player':
                text = "You are revitalised!"
            else:
                text = f"{target.phrase} is revitalised!"
            target.area.post(AlertMessage(text))
        else:
            if target.faction == 'player':
                raise Impossible("You are already at full health.")
            else:
                raise Impossible(f"{target.phrase} is already at full health.")


class StrangeMoss(Consumable):
    """A single-use health boost"""

    def __init__(self, x=0, y=0, area=None):
        super().__init__(name="Moss lump",
                         description="A lump of edible moss.",
                         verb="eat",
                         uses=1, x=x, y=y, colour=C["RED"],
                         char="?", area=area)

    def affect(self, target):
        """Boosts the target's health"."""
        target.body.bonus_health += 2
        if target.body.health < target.body.max_health:
            target.body.health = target.body.max_health
        if target.faction == 'player':
            text = "You feel more vital and healthy."
        else:
            text = f"{target.phrase} is strengthened!"
        target.area.post(AlertMessage(text))


class AcidFlask(Consumable):
    """A container of strong acid."""

    def __init__(self, x=0, y=0, area=None):
        super().__init__("Acid flask",
                         "A stoppered flask of powerful acid.", "drink",
                         1, x, y, "!", C["GREEN"], area)
        self.impact_radius = 3

    def affect(self, target):
        """Burns the consumer's insides."""
        if target.faction == 'player':
            text = "The acid burns your insides!"
        else:
            text = f"{target.phrase} is burnt by the acid!"
        target.area.post(CombatMessage(text))
        target.body.take_damage(10)

    def impact(self):
        """When thrown, splashes acid over the nearby area."""

        text = f"The {self.name} shatters on impact!"
        self.area.post(AlertMessage(text))

        # Get the affected tiles
        tiles = self.area.get_tiles_in_range(self.x,
                                             self.y,
                                             self.impact_radius)

        # For each tile
        for tile in tiles:
            entity = self.area.get_blocker_at_location(*tile)
            if entity:
                report = f"Acid splashes over the {entity.name}!"
                self.area.post(CombatMessage(report))
                entity.body.take_damage(2)

        # Destroy the flask
        self.destroy()
