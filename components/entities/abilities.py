"""This file contains the implementation of the Ability class and its
related subclasses. Abilities can be added and removed from an entity,
and the entity can use them to affect the world"""

from ..environments.features import AcidBlob


class Ability:
    """An in-game ability."""
    def __init__(self, name):
        self.name = name

    def activate(self):
        """Activate the ability."""
        pass


class TargetAbility(Ability):
    """An ability that can be directed."""
    def __init__(self, name, projectile, range):
        super().__init__(name)
        self.projectile = projectile
        self.range = range


class AcidSpit(TargetAbility):
    """Spit corrosive acid."""

    def __init__(self):
        super().__init__(name="acid spit",
                         projectile=AcidBlob(),
                         range=3)
