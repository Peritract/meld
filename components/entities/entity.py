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
from ..items.corpse import Corpse


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

    @property
    def dead(self):
        return self.body.health <= 0

    def take_action(self, area):
        """Acts in the game world."""

        # Pass the request to the AI
        decision = self.mind.make_decision(area)

        # Act on the decisions
        if isinstance(decision, Wait):
            self.wait()
        elif isinstance(decision, Move):
            self.move(decision.dx, decision.dy)
        elif isinstance(decision, Attack):
            self.attack(decision.other, area)

    def move(self, dx, dy):
        """Alters the entity's position by a given amount."""
        self.x += dx
        self.y += dy

    def attack(self, other, area):
        """Attacks another entity."""

        # Subtract health
        other.body.health -= 1

        # Post a message
        report = Message(f"The {self.name} savages the {other.name}", C["RED"])
        area.post_message(report)

        # If the other should die, make that happen
        if other.dead:
            other.die(area)

    def die(self, area):
        # Removes the entity from the game, replacing it with a corpse.
        area.contents.remove(self)
        area.contents.add(Corpse(self.name, self.x, self.y))
        area.post_message(Message(f"The {self.name} dies in agony."))

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
