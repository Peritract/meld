"""This file contains the implementation of the Item class and the basic
item subclasses."""

from ..utilities.object import Object
from ..utilities.constants import COLOURS as C
from ..utilities.messages import CombatMessage


class Item(Object):
    """A basic item."""

    def __init__(self, name, description, x=0, y=0,
                 char="€", colour=C["TEMP"], blocks=False, area=None):
        super().__init__(name, description, x, y, char, colour, blocks, area)

    def impact(self):
        """Landing or being smashed."""
        pass

    def destroy(self):
        """Remove from the game."""
        if self.area:
            self.area.remove_contents(self)
            self.area = None


class Equippable(Item):
    """An equippable item."""

    def __init__(self, name, description, x=0, y=0,
                 char="/", colour=C["TEMP"], area=None):
        super().__init__(name, description, x, y,
                         char, colour, area)
        self.equipped = False


class Weapon(Equippable):
    """An equippable weapon."""

    def __init__(self, name, description, damage, x=0, y=0,
                 char="/", colour=C["TEMP"], verb="strike", area=None):
        super().__init__(name, description, x, y,
                         char, colour, area)
        self.damage = damage
        self.verb = verb

    def impact(self):
        """When thrown, damages blocking entities on the same tile."""

        entity = self.area.get_blocker_at_location(self.x, self.y)

        if entity and entity.body:
            text = f"The {self.name} {self.verb} the {entity.name}."
            self.area.post_message(CombatMessage(text))
            entity.body.take_damage(self.damage)

    def attack(self, agg, vic):
        """Make an attack."""

        verb = self.verb if agg.faction != "player" else self.verb[:-1]
        report = f"The {agg.phrase} {verb} strikes at the {vic.phrase}!"
        agg.area.post_message(CombatMessage(report))
        vic.body.take_damage(self.damage)


class Armour(Equippable):
    """An equippable clothing item."""

    def __init__(self, name, description, x=0, y=0,
                 char="/", colour=C["TEMP"], area=None):
        super().__init__(name, description, x, y,
                         char, colour, area)


class Consumable(Item):
    """An item that is consumed on use."""

    def __init__(self, name, description, verb="use", uses=1, x=0, y=0,
                 char="!", colour=C["TEMP"], area=None):
        super().__init__(name, description, x, y, char, colour, area)
        self.uses = uses
        self.verb = verb

    @property
    def description_text(self):
        uses = f"{self.uses} uses" if self.uses > 1 else "1 use"
        return self.description + f" {uses} remaining."

    def use(self, target):
        """Uses the item"""
        if self.uses > 0:
            self.affect(target)
            self.uses -= 1

    def affect(self, target):
        """Applies the item's effect to the target."""
        raise NotImplementedError()
