"""This file contains the implementation of the Corpse class."""

from .items import Item
from ..utilities.constants import colours as C


class Corpse(Item):

    def __init__(self, name, x, y, area=None):
        super().__init__("Corpse",
                         f"A dead {name}.",
                         x, y, "%",
                         C["GREY"], area)
