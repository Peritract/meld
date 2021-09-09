"""
This file contains the implementation of the Body class.
This class stores physical information about in-game entities.
"""

from random import choice
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
        self.instability = 90
        
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

    def create_corpse(self):
        """Create an appropriate corpse."""
        types = {x.type for x in self.parts}
        return Corpse(name=self.owner.name, x=self.owner.x, y=self.owner.y, types=types)

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

    def update(self):
        """Runs every turn, checking for changes."""
        if self.instability >= 100:
            mutation = self.select_mutation()
            print(mutation)
            self.instability /= 2

    def can_mutate(self, part):
        """Checks if a mutation is possible with current attributes."""

        # Disallow any duplicates.
        if any([isinstance(x, part) for x in self.parts]):
            return False
        else:
            return True

    def select_mutation(self):
        """Chooses a possible mutation from the list."""
        
        # Get the current body parts & affinities
        current_parts = self.parts
        current_types = self.affinities

        for part in parts:
            print(part, self.can_mutate(part))

        valid_parts = []

        return choice(valid_parts)
