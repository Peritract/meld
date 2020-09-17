"""This file contains the implementations of the various
equippable items.
"""

from .equippable import Equippable
from ..utilities.constants import colours as C


class Cudgel(Equippable):
    """A simple wooden club."""

    def __init__(self, x, y):
        super().__init__("cudgel", "weapon", x, y,
                         "/", C["BROWN"])


class Robe(Equippable):
    """A woollen robe."""

    def __init__(self, x, y):
        super().__init__("robe", "armour", x, y,
                         "[", C["BROWN"])
