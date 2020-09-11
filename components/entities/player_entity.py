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
                 mind=None,
                 body=Body,
                 char="@",
                 colour=tcod.white,
                 blocks=True):
        super().__init__(name, x, y, faction, mind, body, char, colour, blocks)

    def take_action(self, instruction, area):
        """Takes an action based on player input."""

        # If the instruction has a direction
        if isinstance(instruction, Surge):

            # Intepret the action based on area context
            action = self.interpret_surge(instruction, area)

            # Holder for a potential message
            message = None

            # Act on the interpretation
            if isinstance(action, Move):
                message = self.move(action.dx, action.dy)
            elif isinstance(action, Attack):
                message = self.attack(action.other)

        elif isinstance(instruction, Wait):
            message = self.wait()

        # If a message needs posting
        if message:
            area.post_message(message)

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

            # If it's passable
            if area.is_passable(target_x, target_y):
                # Make a move
                return Move(instruction.dx, instruction.dy)