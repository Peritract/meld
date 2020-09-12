"""
    This file contains the implementation of the base Entity class;
    An entity is any object more complex than a simple physical item.
"""

from ..utilities.object import Object
from ..utilities.message_log import Message
from .body import Body
from .minds.mind import Mind
from .actions import Wait, Move, Attack
import tcod
import numpy as np
from ..utilities.constants import colours as C


class Entity(Object):
    """The base class for all animate game objects"""

    def __init__(self,
                 name="entity",
                 x=0,
                 y=0,
                 faction="neutral",
                 mind=Mind,
                 body=Body,
                 char="&",
                 colour=tcod.lime,
                 blocks=True):
        super().__init__(name, x, y, char, colour, blocks)
        self.faction = faction
        self.body = body()
        self.body.owner = self
        if mind:
            self.mind = mind()
            self.mind.owner = self

    def take_action(self, area):
        """Acts in the game world."""

        # Pass the request to the AI
        decision = self.mind.make_decision(area)

        # Holder for a potential message
        message = None

        # Act on the decisions
        if isinstance(decision, Wait):
            message = self.wait()
        elif isinstance(decision, Move):
            message = self.move(decision.dx, decision.dy)
        elif isinstance(decision, Attack):
            message = self.attack(decision.other)

        # If a message was created,
        if message:
            # Post it
            area.post_message(message)

    def move(self, dx, dy):
        """Alters the entity's position by a given amount."""
        self.x += dx
        self.y += dy

    def attack(self, other):
        """Attacks another entity."""

        # Subtract health
        other.body.health -= 1

        # Return a message
        return Message(f"The {self.name} savages the {other.name}", C["RED"])

    def wait(self):
        """Passes the turn."""
        pass

    def get_tile_costs(self, level):
        """Calculate the cost of movement around the level
        for this specific."""

        # Make a copy of the passable map
        cost = np.array(level.tiles["passable"], dtype=np.int8)

        # Squares containing entities have a higher cost
        # - discourage routing through them
        for entity in level.entities:
            if entity.blocks and cost[entity.x, entity.y]:
                cost[entity.x, entity.y] += 10

        # Return the cost map
        return cost
