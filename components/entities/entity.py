"""
    This file contains the implementation of the base Entity class;
    An entity is any object more complex than a simple physical item.
"""

from ..utility.object import Object
from ..utility.position import Position
from .minds import Mind
from ..utility.actions import Movement


class Entity(Object):
    """The base class for all animate game objects"""

    def __init__(self, name="entity", position=Position(0, 0), mind=Mind):
        """Sets internal properties"""
        Object.__init__(self, position)
        self.name = name

        # Set up the entity's turn-taking logic
        self.mind = mind()
        self.mind.owner = self

    def move(self, dx, dy):
        """Alters the entity's position by a given amount."""
        self.position.x += dx
        self.position.y += dy

    def take_action(self, level):
        """Takes a turn."""

        # Ask the player/AI to make a decision
        decision = self.mind.take_action(level)

        # Act on the decision
        if isinstance(decision, Movement):
            self.move(decision.dx, decision.dy)
