"""
This file contains the implementation of the Body class.
This class stores physical information about in-game entities.
"""

from ...utilities.messages import CombatMessage
from .body_parts import *
from ...items.corpse import Corpse
from collections import defaultdict

class Body:

    def __init__(self,
                 eyes=HumanEyes,
                 manipulators=HumanHands,
                 propulsors=HumanLegs,
                 exterior=HumanSkin):

        # The various body parts
        self.eyes = eyes()
        self.manipulators = manipulators()
        self.propulsors = propulsors()
        self.exterior = exterior()

        # Container for all body parts
        self.parts = [self.eyes, self.manipulators, self.propulsors, self.exterior]

        # Health
        self.bonus_health = 0
        self.health = self.max_health

        # Instability and mutation
        self.affinities = defaultdict(lambda: 0)
        self.instability = 0
        
    # Properties derived from body parts

    @property
    def view_radius(self):
        return self.eyes.view_radius

    @property
    def can_equip_weapons(self):
        return self.manipulators.can_equip

    @property
    def strength(self):
        return self.manipulators.strength

    @property
    def speed(self):
        return self.propulsors.speed

    @property
    def max_health(self):
        return self.exterior.max_health + self.bonus_health

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

    def become_corpse(self):

        types = {x['type'] for x in self.parts}
        return Corpse(self.owner.name, self.owner.x, self.owner.y, types)

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

    def increase_affinities(self, types):
        """Become more attuned to different types of creature."""
        for thing in types:
            self.affinities[thing] += 10