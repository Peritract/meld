"""This file contains the implementations of the various
equippable items.
"""

from .items import Weapon, Armour
from ..utilities.constants import COLOURS as C


class Cudgel(Weapon):
    """A simple wooden club."""

    def __init__(self, x=0, y=0, area=None):
        super().__init__("Cudgel",
                         "A short, weighty club.",
                         2,
                         x, y,
                         "/", C["BROWN"], "strike", area)


class Robe(Armour):
    """A woollen robe."""

    def __init__(self, x=0, y=0, area=None):
        super().__init__("Robe",
                         "A scratchy wool robe.",
                         x, y,
                         "[", C["BROWN"], area)
