"""This file contains the implementation of the basic
equipment class and its immediate descendants.
"""

from .item import Item
from ..utilities.constants import colours as C
from ..utilities.messages import Message


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

        if entity:
            text = f"The {self.name} strikes the {entity.name}."
            self.area.post_message(Message(text, C["RED"]))
            entity.take_damage(self.damage)


class Armour(Equippable):
    """An equippable clothing item."""

    def __init__(self, name, description, x, y,
                 char="/", colour=C["TEMP"], area=None):
        super().__init__(name, description, x, y,
                         char, colour, area)
