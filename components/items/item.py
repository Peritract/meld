"""This file contains the implementation of the Item object.
Mostly, at present, just a pass-through class for specific items.
"""

from ..utilities.object import Object
from ..utilities.constants import colours as C


class Item(Object):

    def __init__(self, name, x, y, usable=False, equippable=False,
                 char="€", colour=C["GREY"], blocks=False):
        super().__init__(name, x, y, char, colour, blocks)
        self.usable = usable
        self.equippable = equippable
