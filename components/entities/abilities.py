"""This file contains the implementation of the Ability class and its
related subclasses. Abilities can be added and removed from an entity,
and the entity can use them to affect the world"""


class Ability:
    """An in-game ability."""
    def __init__(self, name):
        self.name = name

    def activate(self):
        """Activate the ability."""
        pass


class AcidSpit(Ability):
    """Spit corrosive acid."""

    def __init__(self):
        super().__init__("acid spit")
