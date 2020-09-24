"""
This file contains the implementation of the Body class.
This class stores physical information about in-game entities.
"""

from ..utilities.messages import Message
from ..utilities.constants import COLOURS as C


class Body:

    def __init__(self,
                 health=5,
                 strength=5,
                 view_radius=8):
        self.health = health
        self.max_health = health
        self.view_radius = view_radius
        self.carry_capacity = 3
        self.strength = strength

    @property
    def dead(self):
        if self.health <= 0:
            return True

    def heal(self, amount):
        """Replenishes health."""
        self.health = min(self.max_health, self.health + amount)

    def take_damage(self, amount):
        """Takes damage."""
        self.health = max(0, self.health - amount)

        # Check for permanent consequences
        if self.dead:
            self.owner.die()

    def attack(self, other):
        """Attack another entity physically."""

        report = f"The {self.owner.name} flails at the {other.name}!"
        self.owner.area.post_message(Message(report, C["RED"]))

        other.body.take_damage(1)
