"""
    This file contains the implementation of the base Entity class;
    An entity is any object more complex than a simple physical item.
"""

from ..utility.object import Object
from .minds import Mind
from .bodies import Body
from ..utility.actions import Move, Attack, Wait
from ..utility.event_log import Event, Death
from ..utility.message_log import Message
from ..items.items import Corpse
import tcod


class Entity(Object):
    """The base class for all animate game objects"""

    def __init__(self,
                 name="entity",
                 position=(0, 0),
                 mind=Mind,
                 body=Body,
                 faction="neutral",
                 char="&",
                 colour=tcod.lime,
                 blocks=True):
        """Sets internal properties"""
        Object.__init__(self, name, position, char, colour, blocks)

        # Set up the entity's turn-taking logic
        self.mind = mind()
        self.mind.owner = self

        # Set up the entity's loyalties
        self.faction = faction

        # Set up the entity's physical form
        self.body = Body()
        self.body.owner = self

    def move(self, dx, dy):
        """Alters the entity's position by a given amount."""
        self.x += dx
        self.y += dy

    def attack(self, other):
        """Attempts to damage another entity."""

        # Holder for results
        results = []

        damage = self.body.attack - other.body.defence
        results.append(Message(f"The {self.name} bashes the {other.name}!"))
        if damage > 0:
            other.take_damage(damage)
            if other.body.health <= 0:
                results.append(Death(other))

        return results

    def take_damage(self, amount):
        """Reduces health."""
        self.body.health -= amount

    def die(self, level):
        level.entities.remove(self)
        level.items.append(Corpse((self.x, self.y), self.name))
        return Message(f"The {self.name} dies in agony.")

    def take_action(self, level, message_log, event_log):
        """Takes a turn."""

        # Ask the player/AI to make a decision
        decision = self.mind.take_action(level)

        # Act on the decision
        if isinstance(decision, Move):
            results = self.move(decision.dx, decision.dy)

        elif isinstance(decision, Attack):
            results = self.attack(decision.other)

        elif isinstance(decision, Wait):
            results = [Message(f"The {self.name} waits.")]

        # Send turn results in the right direction
        if results:
            for result in results:
                if isinstance(result, Message):
                    message_log.add_message(result)
                elif isinstance(result, Event):
                    event_log.add_event(result)
