"""This file contains the implementations of the various
equippable items.
"""

from .items import Weapon, Armour
from ..utilities.constants import COLOURS as C


class Cudgel(Weapon):
    """A simple wooden club."""

    def __init__(self, x, y, area=None):
        super().__init__("Cudgel",
                         "A short, weighty club.",
                         2,
                         x, y,
                         "/", C["BROWN"], area)


class Robe(Armour):
    """A woollen robe."""

    def __init__(self, x, y, area=None):
        super().__init__("Robe",
                         "A scratchy wool robe.",
                         x, y,
                         "[", C["BROWN"], area)
