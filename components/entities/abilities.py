"""This file contains the implementation of the Ability class and its
related subclasses. Abilities can be added and removed from an entity,
and the entity can use them to affect the world"""

from ..environments.features import AcidBlob


class Ability:
    """An in-game ability."""
    def __init__(self, name, cooldown=0):
        self.name = name
        self.cooldown = cooldown
        self.delay = 0

    @property
    def ready(self):
        return self.delay == 0

    def activate(self):
        """Activate the ability."""
        pass

        # Set the timer
        self.delay = self.cooldown

    def update(self):
        """Update each turn."""

        # If there's a cooldown active, delay it.
        if self.delay > 0:
            self.delay -= 1


class TargetAbility(Ability):
    """An ability that can be directed."""
    def __init__(self, name, ammunition, range, cooldown):
        super().__init__(name, cooldown)
        self.ammunition = ammunition
        self.range = range

    @property
    def projectile(self):
        """Return a new object to fire."""
        return self.ammunition()


class AcidSpit(TargetAbility):
    """Spit corrosive acid."""

    def __init__(self):
        super().__init__(name="acid spit",
                         ammunition=AcidBlob,
                         range=3,
                         cooldown=3)
