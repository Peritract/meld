"""This file contains the implementation of the Item class and the basic
item subclasses."""

from ..utilities.object import Object
from ..utilities.constants import COLOURS as C
from ..utilities.messages import Message


class Item(Object):
    """A basic item."""

    def __init__(self, name, description, x, y,
                 char="€", colour=C["TEMP"], blocks=False, area=None):
        super().__init__(name, description, x, y, char, colour, blocks, area)

    def impact(self):
        """Landing or being smashed."""
        pass


class Equippable(Item):
    """An equippable item."""

    def __init__(self, name, description, x, y,
                 char="/", colour=C["TEMP"], area=None):
        super().__init__(name, description, x, y,
                         char, colour, area)
        self.equipped = False


class Weapon(Equippable):
    """An equippable weapon."""

    def __init__(self, name, description, damage, x, y,
                 char="/", colour=C["TEMP"], area=None):
        super().__init__(name, description, x, y,
                         char, colour, area)
        self.damage = damage

    def impact(self):
        """When hit, damages blocking entities on the same tile."""

        entity = self.area.get_blocker_at_location(self.x, self.y)

        if entity and entity.body:
            text = f"The {self.name} strikes the {entity.name}."
            self.area.post_message(Message(text, C["RED"]))
            entity.body.take_damage(self.damage)


class Armour(Equippable):
    """An equippable clothing item."""

    def __init__(self, name, description, x, y,
                 char="/", colour=C["TEMP"], area=None):
        super().__init__(name, description, x, y,
                         char, colour, area)


class Consumable(Item):
    """An item that is consumed on use."""

    def __init__(self, name, description, uses, x, y,
                 char="!", colour=C["TEMP"], area=None):
        super().__init__(name, description, x, y, char, colour, area)
        self.uses = uses

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
