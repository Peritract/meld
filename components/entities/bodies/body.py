"""
This file contains the implementation of the Body class.
This class stores physical information about in-game entities.
"""

from ...utilities.messages import CombatMessage
from .body_parts import *

class Body:

    def __init__(self,
                 base_health=20,
                 strength=5,
                 speed=10,
                 eyes=HumanEyes,
                 manipulators=HumanHands,
                 propulsors=HumanLegs):
        self.health = base_health
        self.max_health = base_health
        self.strength = strength

        # The various body parts
        self.eyes = eyes()
        self.manipulators = manipulators()
        self.propulsors = propulsors()

    # Properties derived from body parts

    @property
    def view_radius(self):
        return self.eyes.view_radius

    @property
    def can_equip_weapons(self):
        return self.manipulators.can_equip

    @property
    def speed(self):
        return self.propulsors.speed

    # Other properties

    @property
    def carry_capacity(self):
        return 2 + self.strength // 2

    @property
    def throw_range(self):
        return self.strength + 2

    @property
    def dead(self):
        return self.health <= 0

    def heal(self, amount):
        """Replenish health."""
        self.health = min(self.max_health, self.health + amount)

    def take_damage(self, amount):
        """Take damage."""
        self.health = max(0, self.health - amount)

        # Check for permanent consequences
        if self.dead:
            self.owner.die()

    def on_contact(self, other):
        """Skin-to-skin contact."""
        pass

    def attack(self, other):
        """Attack another entity physically."""

        verb = self.manipulators.verb
        report = f"{self.owner.phrase} {verb + self.owner.verb_addition} at {other.phrase}!"
        report = report.capitalize()
        self.owner.area.post(CombatMessage(report))

        # Process any skin contact effects.
        self.on_contact(other)
        other.body.on_contact(self)

        # Apply damage
        other.body.take_damage(self.manipulators.damage)
