"""This file contains the implementation of the Ability class and its
related subclasses. Abilities can be added and removed from an entity,
and the entity can use them to affect the world"""

from ..environments.features import AcidBlob
from ..entities.conditions import Lure
from ..utilities.messages import AlertMessage


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
    """An ability that needs targetting."""

    def __init__(self, name, aim_range, cooldown=0):
        super().__init__(name, cooldown)
        self.range = aim_range


class FireAbility(TargetAbility):
    """An ability that can fire a projectile."""
    def __init__(self, name, ammunition, aim_range, cooldown):
        super().__init__(name, aim_range, cooldown)
        self.ammunition = ammunition

    @property
    def projectile(self):
        """Return a new object to fire."""
        return self.ammunition()


class SpellAbility(TargetAbility):
    """A range ability with no projectile."""
    def __init__(self, name, aim_range, cooldown):
        super().__init__(name, aim_range, cooldown)

    def apply(self):
        """The actual effect."""
        raise NotImplementedError()


class AcidSpit(FireAbility):
    """Spit corrosive acid."""

    def __init__(self):
        super().__init__(name="acid spit",
                         ammunition=AcidBlob,
                         aim_range=3,
                         cooldown=3)


class LurePrey(SpellAbility):
    """Lure an entity towards you."""

    def __init__(self):
        super().__init__(name="lure prey",
                         aim_range=6,
                         cooldown=8)

    def apply(self, source, target):
        """Overpower the entity's normal AI."""

        # Get the entity at the location
        entity = source.area.get_blocker_at_location(*target)
        if entity:
            entity.conditions.add(Lure(5, entity, source))
        else:
            report = "There is no effect."
            source.area.post(AlertMessage(report))
