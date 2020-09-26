"""This file contains the implementation of the Corpse class."""

from .items import Item
from ..utilities.constants import COLOURS as C


class Corpse(Item):

    def __init__(self, name="body", x=0, y=0, area=None):
        super().__init__("Corpse",
                         f"A dead {name}.",
                         x, y, "%",
                         C["GREY"], area)
