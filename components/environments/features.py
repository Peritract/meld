"""This file contains the implementation of the Features class and related
subclasses. Features are non-item, non-entity objects in the world, such
as stairs or monster spawners."""

from ..utilities.object import Object
from ..utilities.constants import COLOURS as C, RenderOrder


class Feature(Object):
    """An independent, non-sentient object."""

    def __init__(self, name="feature", description="An object in the world",
                 x=0, y=0, char="£", colour=C["TEMP"], blocks=False,
                 area=None):
        super().__init__(name, description, x, y, char, colour, blocks,
                         area, RenderOrder.FEATURE)

    def interact(self, entity):
        """Respond to an entity's action."""
        pass

    def act(self):
        """Act without prompting."""
        pass


class Stairs(Feature):
    """A path between areas of the dungeon."""

    def __init__(self, x, y, area, target):
        self.target = target

        name = "stairs down" if area.area_id < target.area_id else "stairs up"
        description = "Stairs down into the darkness." \
                      if name == "stairs down" \
                      else "Stairs up towards the light."
        char = "<" if name == "stairs down" else ">"

        super().__init__(name, description, x, y, char, colour=C["GREY"],
                         blocks=False, area=area)

    def interact(self, entity):
        """Move an entity between areas."""
        entity.change_area(self.target)
