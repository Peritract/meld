"""This file contains the implementation of the Features class and related
subclasses. Features are non-item, non-entity objects in the world, such
as stairs or monster spawners. They cannot be picked up."""

from ..utilities.object import Object
from ..utilities.constants import COLOURS as C, RenderOrder
from ..utilities.messages import CombatMessage


class Feature(Object):
    """An independent, non-sentient object."""

    def __init__(self, name="feature", description="An object in the world",
                 x=0, y=0, char="£", colour=C["TEMP"], blocks=False,
                 interactable=True, area=None, update_speed=10, mappable=False):
        super().__init__(name, description, x, y, char, colour, blocks,
                         area, RenderOrder.FEATURE)
        self.interactable = interactable
        self.readiness = 100
        self.update_speed = update_speed
        self.mappable = True

    def interact(self, entity):
        """Respond to an entity's action."""
        pass

    def act(self):
        """Act without prompting."""
        pass

    def update(self):
        """Change state in response to time."""
        pass

    def check_update(self):
        """Runs updates regularly"""
        if self.readiness >= 100:
            self.update()
            self.readiness -= 100
        else:
            self.readiness += self.update_speed


class MappedFeature(Feature):
    """A feature that appears on the map once discovered."""

    def __init__(self, name="mapped feature",
                 description="An object worth remembering.",
                 x=0, y=0, char="_", colour=C["TEMP"],
                 blocks=False, interactable=False, area=None, duration=0, update_speed=10,
                 discovered=False):
        self.discovered = discovered
        super().__init__(name, description, x, y, char, colour=colour,
                    blocks=blocks, interactable=interactable, area=area, mappable=True)


class TemporaryFeature(Feature):
    """A feature with an expiry date."""

    def __init__(self, name="temporary feature",
                 description="A temporary object in the world.",
                 x=0, y=0, char="_", colour=C["TEMP"], blocks=False,
                 interactable=False, area=None, duration=0, update_speed=10):
        super().__init__(name, description, x, y, char, colour,
                         blocks=False, interactable=interactable,
                         area=area, update_speed=update_speed)
        self.duration = duration

    def update(self):
        """Runs every turn."""
        self.duration -= 1
        if self.duration <= 0:
            self.destroy()


class Stairs(MappedFeature):
    """A path between areas of the dungeon."""

    def __init__(self, x, y, area, target):
        self.target = target

        name = "stairs down" if area.area_id < target.area_id else "stairs up"
        description = "Stairs down into the darkness." \
                      if name == "stairs down" \
                      else "Stairs up towards the light."
        char = "<" if name == "stairs down" else ">"

        super().__init__(name, description, x, y, char, colour=C["GREY"],
                         blocks=False, interactable=True, area=area)

    def interact(self, entity):
        """Move an entity between areas."""
        entity.change_area(self.target)


class AcidBlob(TemporaryFeature):
    """A blob of corrosive acid."""

    def __init__(self, x=0, y=0, damage=3, duration=3, area=None,
                 update_speed=10):
        super().__init__("acid blob", "a blob of corrosive acid",
                         x, y, "_", C["GREEN"], False, False, area,
                         duration, update_speed)
        self.damage = damage

    def act(self):
        """Harm an entity in the same location."""

        # If there is an entity in the location
        entity = self.area.get_blocker_at_location(*self.loc)

        if entity:
            report = f"Acid burns {entity.phrase}!"
            self.area.post(CombatMessage(report))
            entity.body.take_damage(self.damage)

            # Destroy self
            self.destroy()

    def impact(self):
        """Landing in a new location."""

        # Check for an entity to damage
        self.act()

    def update(self):
        """Runs every turn."""

        self.act()

        super().update()
