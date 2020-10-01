"""This file contains the implementation of the base Entity class;
An entity is any object with a mind.
"""

from ..utilities.object import Object
from ..utilities.constants import COLOURS as C, RenderOrder
from ..utilities.messages import DeathMessage
from .body import Body
from .minds.mind import Mind
from .actions import Wait, Move, Attack, PickUp
import numpy as np
from ..items.corpse import Corpse
from ..environments.features import Stairs
from ..items.items import Equippable, Weapon, Armour


class Entity(Object):
    """The base class for all animate game objects"""

    def __init__(self,
                 name="entity",
                 description="A living being.",
                 x=0,
                 y=0,
                 faction="neutral",
                 mind=Mind,
                 body=Body,
                 char="&",
                 colour=C["TEMP"],
                 blocks=True,
                 area=None):
        super().__init__(name, description, x, y, char, colour,
                         blocks, area, RenderOrder.ENTITY)
        self.faction = faction
        self.body = body()
        self.body.owner = self
        if mind:
            self.mind = mind()
            self.mind.owner = self

        # Empty inventory by default
        self.inventory = set()

        # Empty conditions by default
        self.conditions = set()

        # Empty abilities by default
        self.abilities = set()

    @property
    def phrase(self):
        return f"the {self.name}"

    @property
    def inventory_full(self):
        return self.body.carry_capacity <= len(self.inventory)

    @property
    def equipment(self):
        """Returns all the currently-held equipment."""
        return [x for x in self.inventory if isinstance(x, Equippable)]

    @property
    def weapon(self):
        """Returns the currently equipped weapon."""
        for item in self.equipment:
            if item.equipped and isinstance(item, Weapon):
                return item

    @property
    def armour(self):
        """Returns the currently equipped armour."""
        for item in self.equipment:
            if item.equipped and isinstance(item, Armour):
                return item

    def take_action(self):
        """Acts in the game world."""

        # Pass the request to the AI
        decision = self.mind.make_decision()

        # Act on the decisions
        if isinstance(decision, Wait):
            self.wait()
        elif isinstance(decision, Move):
            self.move(decision.dx, decision.dy)
        elif isinstance(decision, Attack):
            self.attack(decision.other)
        elif isinstance(decision, PickUp):
            self.pick_up()

    def pick_up(self, item):
        """Adds an item to the inventory."""
        self.inventory.add(item)

        # If the item was present in the area, remove it from there:
        if item in self.area.contents:
            self.area.remove_contents(item)

    def drop(self, item):
        """Removes an item from the inventory."""
        self.inventory.remove(item)

        # Place it in the current tile
        item.x, item.y = self.x, self.y

        # Unequip it, if it was equipped
        if isinstance(item, Equippable) and item.equipped:
            item.equipped = False

        self.area.add_contents(item)

    def equip(self, item):
        """Equips an item, unequipping any item of the same type."""

        # Unequip the previous weapon, if item is a weapon
        if isinstance(item, Weapon) and self.weapon:
            self.weapon.equipped = False

        # Unequip the previous armour, if item is armour
        if isinstance(item, Armour) and self.armour:
            self.armour.equipped = False

        # Equip the item
        item.equipped = True

    def unequip(self, item):
        """Unequip an item."""

        item.equipped = False

    def move(self, dx, dy):
        """Alters the entity's position by a given amount."""
        self.x += dx
        self.y += dy

    def attack(self, other):
        """Attacks another entity."""

        # Make the attack
        if self.weapon:

            # Attack with the weapon
            self.weapon.attack(self, other)
        else:

            # Attack unarmed
            self.body.attack(other)

    def die(self):
        """Removes the entity from the game, replacing it with a corpse."""

        # Replace the entity with a corpse
        self.area.contents.remove(self)
        self.area.contents.add(Corpse(self.name, self.x, self.y))

        # Drop the entity's inventory
        for item in list(self.inventory):
            self.drop(item)

        # Log the death
        text = f"{self.phrase} dies in agony.".capitalize()
        self.area.post(DeathMessage(text))

    def wait(self):
        """Passes the turn."""
        pass

    def use(self, item):
        """Uses an item on the entity."""

        # Call the item's use method
        item.use(self)

        # If the item is used up, remove it
        if item.uses <= 0:
            self.inventory.remove(item)

    def get_tile_costs(self):
        """Calculate the cost of movement around the area
        for this specific entity."""

        # Make a copy of the passable map
        cost = np.array(self.area.tiles["passable"], dtype=np.int8)

        # Squares containing entities have a higher cost
        # - discourage routing through them
        for entity in self.area.entities:
            if entity.blocks and cost[entity.x, entity.y]:
                cost[entity.x, entity.y] += 10

        # Return the cost map
        return cost

    def throw(self, item, target):
        """Throw an object towards a location."""

        self.inventory.remove(item)

        # Unequip it, if it was equipped
        if isinstance(item, Equippable) and item.equipped:
            item.equipped = False

        # Add it to the area
        self.area.add_contents(item)

        # Move it to the right tile
        item.x, item.y = target

        item.impact()

    def change_area(self, target):
        """Move from one area to another."""

        # Log the old id for location matching
        old_id = self.area.area_id

        # Remove self from current area
        self.area.remove_contents(self)

        # Add self to the new area
        target.add_contents(self)

        # Switch to the correct location
        for feature in self.area.features:
            if isinstance(feature, Stairs) \
                    and feature.target.area_id == old_id:
                self.set_loc(feature.x, feature.y)

    def interact(self):
        """Interact with a feature."""

        # If a feature is present
        feature = self.area.get_interactable_feature_at_location(*self.loc)
        if feature:
            feature.interact(self)

    def add_condition(self, condition):
        """Add a condition to the entity."""

        self.conditions.add(condition)
        condition.attach(self)

    def add_ability(self, ability):
        """Gain a new ability."""

        self.abilities.add(ability)

    def fire(self, projectile, target):
        """Fire a projectile."""

        # Add it to the area
        self.area.add_contents(projectile)

        # Move it to the right tile
        projectile.x, projectile.y = target

        projectile.impact()

    def update(self):
        """Carry out regular checks and actions."""

        # Apply each condition
        for condition in self.conditions:
            condition.apply()

        # Update abilities
        for ability in self.abilities:
            ability.update()
