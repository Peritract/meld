"""This file contains the various item types found in the game."""

from ..utility.object import Object

import tcod


class Corpse(Object):
    """A creature's corpse."""
    def __init__(self, position, name="",
                 colour=tcod.red):
        super().__init__(name, position,
                         colour=colour,
                         blocks=False)
