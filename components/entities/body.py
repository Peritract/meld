"""
This file contains the implementation of the Body class.
This class stores physical information about in-game entities.
"""

from ..utilities.messages import CombatMessage


class Body:

    def __init__(self,
                 health=5,
                 strength=5,
                 speed=10,
                 view_radius=8):
        self.health = health
        self.max_health = health
        self.strength = strength
        self.speed = speed
        self.view_radius = view_radius

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

        verb = "flails" if self.owner.faction != "player" else "flail"
        report = f"{self.owner.phrase} {verb} at {other.phrase}!"
        report = report.capitalize()
        self.owner.area.post(CombatMessage(report))

        # Process any skin contact effects.
        self.on_contact(other)
        other.on_contact(self)

        # Apply damage
        other.body.take_damage(1)
