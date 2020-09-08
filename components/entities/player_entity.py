"""
This file contains the implementation of the Player class.
This is the game's player character.
"""

from .entity import Entity
from .actions import Move, Attack, Wait

import tcod


class Player(Entity):
    """The player character."""

    def __init__(self,
                 name="entity",
                 x=0,
                 y=0,
                 faction="player",
                 char="@",
                 colour=tcod.white,
                 blocks=True):
        super().__init__(name, x, y, faction, char, colour, blocks)

    def take_action(self, instruction):
        """Takes an action based on player input."""

        if isinstance(instruction, Move):
            self.move(instruction.dx, instruction.dy)

        elif isinstance(instruction, Attack):
            self.attack(instruction.other)

        elif isinstance(instruction, Wait):
            self.wait()
