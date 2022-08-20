"""
This file contains the implementation of the Body class.
This class stores physical information about in-game entities.
"""

from random import choice
from ...utilities.messages import CombatMessage, WorldMessage
from .body_parts import parts, HumanEyes, HumanHands, HumanLegs, HumanMouth, HumanSkin
from ...items.corpse import Corpse
from collections import defaultdict

class Body:

    def __init__(self,
                 eyes=HumanEyes,
                 manipulators=HumanHands,
                 propulsors=HumanLegs,
                 exterior=HumanSkin,
                 mouth=HumanMouth):

        # The various body parts
        self.eyes = eyes()
        self.manipulators = manipulators()
        self.propulsors = propulsors()
        self.exterior = exterior()
        self.mouth = mouth()

        # Health
        self.bonus_health = 0
        self.health = self.exterior.max_health

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

    @property
    def parts(self):
        return [self.eyes, self.mouth, self.manipulators, self.propulsors, self.exterior]

    @property
    def abilities(self):
        # List of abilities granted by body parts
        return [x.ability for x in self.parts if hasattr(x, "ability")]

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
        affinities = {x.affinity for x in self.parts}
        return Corpse(name=self.owner.name, x=self.owner.x, y=self.owner.y, affinities=affinities)

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

    def increase_affinities(self, affinities):
        """Become more attuned to different sorts of creature."""
        for thing in affinities:
            self.affinities[thing] += 10

    def update(self):
        """Runs every turn, checking for changes."""
        if self.instability >= 100:
            mutation = self.select_mutation()
            self.mutate(mutation)
            self.instability /= 2

    def is_valid_mutation(self, part):
        """Checks if a mutation is possible with current attributes."""

        # Disallow any duplicates.
        if any([isinstance(x, part) for x in self.parts]):
            return False
        else:
            return True

    def select_mutation(self):
        """Chooses a possible mutation from the list."""

        valid_parts = [p for p in parts if self.is_valid_mutation(p)]

        return choice(valid_parts)

    def mutate(self, part):
        """Actually transforms the body."""
        new_part = part()

        if new_part.type == "mouth":
            old_part = self.mouth
            self.mouth = new_part
        elif new_part.type == "eyes":
            old_part = self.eyes
            self.eyes = new_part
        elif new_part.type == "exterior":
            old_part = self.exterior
            self.exterior = new_part
        elif new_part.type == "manipulators":
            old_part = self.manipulators
            self.manipulators = new_part
        elif new_part.type == "propulsors":
            old_part = self.propulsors
            self.propulsors = new_part

        self.owner.area.post(WorldMessage("You are racked with pain as your form shifts."))
        report = f"{self.owner.possessive_phrase} {old_part.desc} transforms into {new_part.desc}!"
        self.owner.area.post(WorldMessage(report))