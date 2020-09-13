"""
This file contains the implementation of the Player class.
This is the game's player character.
"""

from .entity import Entity
from .actions import Surge, Move, Attack, Wait, PickUp
from ..items.corpse import Corpse
from ..utilities.message_log import Message
from ..entities.body import Body
from ..utilities.exceptions import Impossible

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
                 blocks=True,
                 area=None):
        super().__init__(name, x, y, faction, mind, body,
                         char, colour, blocks, area)

    def take_action(self, instruction):
        """Takes an action based on player input."""

        # If the instruction has a direction
        if isinstance(instruction, Surge):

            # Intepret the action based on area context
            action = self.interpret_surge(instruction)

            # Act on the interpretation
            if isinstance(action, Move):
                self.move(action.dx, action.dy)
            elif isinstance(action, Attack):
                self.attack(action.other)

        elif isinstance(instruction, PickUp):
            self.pick_up()

        elif isinstance(instruction, Wait):
            self.wait()

    def interpret_surge(self, instruction):
        """Interprets an action with a direction based on context."""

        # Get the target coordinates
        target_x = self.x + instruction.dx
        target_y = self.y + instruction.dy

        # If the target is valid
        if self.area.in_bounds(target_x, target_y):

            # Check for an entity at the target location
            occupant = self.area.get_blocker_at_location(target_x, target_y)

            # If there is an occupant
            if occupant:
                return Attack(occupant)

            # If it's free
            if self.area.is_free(target_x, target_y):
                # Make a move
                return Move(instruction.dx, instruction.dy)

        # Invalid surge
        raise Impossible("There is no path that way.")

    def die(self):
        # Removes the entity from the game, replacing it with a corpse.
        # As this is the player, also ends the game
        self.area.contents.remove(self)
        self.area.contents.add(Corpse(self.name, self.x, self.y))
        self.area.post_message(Message(f"The {self.name} dies in agony."))
        self.area.world.engine.set_state("game_over")
