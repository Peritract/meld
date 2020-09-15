"""This file contains the implementation of the base Entity class;
An entity is any object with a mind.
"""

from ..utilities.object import Object
from ..utilities.message_log import Message
from .body import Body
from .minds.mind import Mind
from .actions import Wait, Move, Attack, PickUp
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
                 blocks=True,
                 area=None):
        super().__init__(name, x, y, char, colour, blocks)
        self.faction = faction
        self.body = body()
        self.body.owner = self
        if mind:
            self.mind = mind()
            self.mind.owner = self
        if area:
            self.area = area

        # Empty inventory by default
        self.inventory = set()

    @property
    def dead(self):
        return self.body.health <= 0

    @property
    def inventory_full(self):
        return self.body.carry_capacity <= len(self.inventory)

    def take_action(self):
        """Acts in the game world."""

        # Pass the request to the AI
        decision = self.mind.make_decision()

        # Act on the decisions
        if isinstance(decision, Wait):
            self.wait()
        elif isinstance(decision, Move):
            self.move(decision.dx, decision.dy)
        elif isinstance(decision, Attack):
            self.attack(decision.other)
        elif isinstance(decision, PickUp):
            self.pick_up()

    def pick_up(self, item):
        """Adds an item to the inventory."""
        self.inventory.add(item)
        self.area.contents.remove(item)

    def drop(self, item):
        """Removes an item from the inventory."""
        self.inventory.remove(item)

        # Place it in the current tile
        item.x, item.y = self.x, self.y
        
        self.area.contents.add(item)

    def move(self, dx, dy):
        """Alters the entity's position by a given amount."""
        self.x += dx
        self.y += dy

    def attack(self, other):
        """Attacks another entity."""

        # Subtract health
        other.body.health -= 1

        # Post a message
        report = Message(f"The {self.name} savages the {other.name}", C["RED"])
        self.area.post_message(report)

        # If the other should die, make that happen
        if other.dead:
            other.die()

    def die(self):
        # Removes the entity from the game, replacing it with a corpse.
        self.area.contents.remove(self)
        self.area.contents.add(Corpse(self.name, self.x, self.y))
        self.area.post_message(Message(f"The {self.name} dies in agony."))

    def wait(self):
        """Passes the turn."""
        pass

    def get_tile_costs(self):
        """Calculate the cost of movement around the area
        for this specific entity."""

        # Make a copy of the passable map
        cost = np.array(self.area.tiles["passable"], dtype=np.int8)

        # Squares containing entities have a higher cost
        # - discourage routing through them
        for entity in self.area.entities:
            if entity.blocks and cost[entity.x, entity.y]:
                cost[entity.x, entity.y] += 10

        # Return the cost map
        return cost
