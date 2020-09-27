"""This file contains the implementations of the various
equippable items.
"""

from .items import Weapon, Armour
from ..utilities.constants import COLOURS as C
from ..entities.conditions import Poison
from ..utilities.messages import AlertMessage
from random import random


class Cudgel(Weapon):
    """A simple wooden club."""

    def __init__(self, x=0, y=0, area=None):
        super().__init__("Cudgel",
                         "A short, weighty club.",
                         2,
                         x, y,
                         "/", C["BROWN"], "strikes", area)


class PoisonDagger(Weapon):
    """A curved dagger dipped in strange oils."""

    def __init__(self, x=0, y=0, area=None):
        super().__init__("Poisoned dagger",
                         "A curved dagger dipped in strange oils",
                         1, x, y, "/", C["GREEN"], "stabs", area)
        self.poison_chance = 0.3
        self.poison_damage = 1
        self.poison_duration = 3

    def attack(self, agg, vic):
        """Make an attack."""

        super().attack(agg, vic)

        x = random()
        print(x)
        if x <= self.poison_chance:
            vic.add_condition(Poison(self.poison_duration,
                                     self.poison_damage))

            verb = "has" if vic.faction != "player" else "have"
            report = f"{vic.phrase} {verb} been poisoned!"
            agg.area.post_message(AlertMessage(report))


class Robe(Armour):
    """A woollen robe."""

    def __init__(self, x=0, y=0, area=None):
        super().__init__("Robe",
                         "A scratchy wool robe.",
                         x, y,
                         "[", C["BROWN"], area)
