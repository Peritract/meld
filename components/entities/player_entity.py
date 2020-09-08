"""
This file contains the implementation of the Player class.
This is the game's player character.
"""

from .entity import Entity
from .actions import Surge, Move, Attack, Wait

from ..entities.body import Body

import tcod


class Player(Entity):
    """The player character."""

    def __init__(self,
                 name="entity",
                 x=0,
                 y=0,
                 faction="player",
                 body=Body,
                 char="@",
                 colour=tcod.white,
                 blocks=True):
        super().__init__(name, x, y, faction, body, char, colour, blocks)

    def take_action(self, instruction, area):
        """Takes an action based on player input."""

        # If the instruction has a direction
        if isinstance(instruction, Surge):

            # Intepret the action based on area context
            action = self.interpret_surge(instruction, area)

            # Act on the interpretation
            if isinstance(action, Move):
                self.move(action.dx, action.dy)
            elif isinstance(action, Attack):
                self.attack(action.other)

        elif isinstance(instruction, Wait):
            self.wait()

    def interpret_surge(self, instruction, area):
        """Interprets an action with a direction based on context."""

        # Get the target coordinates
        target_x = self.x + instruction.dx
        target_y = self.y + instruction.dy

        # If the target is valid
        if area.in_bounds(target_x, target_y):

            # Check for an entity at the target location
            occupant = area.get_blocker_at_location(target_x, target_y)

            # If there is an occupant
            if occupant:
                return Attack(occupant)

            # Otherwise, it's a move
            return Move(instruction.dx, instruction.dy)
