"""
    This file contains the implementation of the base Entity class;
    An entity is any object more complex than a simple physical item.
"""

from ..utility.object import Object
from .minds import Mind
from ..utility.actions import Movement

import tcod


class Entity(Object):
    """The base class for all animate game objects"""

    def __init__(self,
                 name="entity",
                 position=(0, 0),
                 mind=Mind,
                 char="&",
                 colour=tcod.lime,
                 blocks=True):
        """Sets internal properties"""
        Object.__init__(self, name, position, char, colour, blocks)

        # Set up the entity's turn-taking logic
        self.mind = mind()
        self.mind.owner = self

    def move(self, dx, dy):
        """Alters the entity's position by a given amount."""
        self.x += dx
        self.y += dy

    def take_action(self, level):
        """Takes a turn."""

        # Ask the player/AI to make a decision
        decision = self.mind.take_action(level)

        # Act on the decision
        if isinstance(decision, Movement):
            self.move(decision.dx, decision.dy)
