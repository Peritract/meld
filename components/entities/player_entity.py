"""
This file contains the implementation of the Player class.
This is the game's player character.
"""

from .entity import Entity
from .actions import (Surge, Wait, PickUp, OpenInventory, Throw,
                      Drop, Use, Equip, Unequip, Handle, Look, OpenMenu)
from ..utilities.messages import Message
from ..entities.body import Body
from ..utilities.exceptions import Impossible
from ..utilities.states.item_selection_menu import ItemSelectionMenu
from ..utilities.states.look_state import LookState
from ..utilities.states.inventory_menu import InventoryMenu
from ..utilities.states.in_game_menu import InGameMenu

import tcod


class Player(Entity):
    """The player character."""

    def __init__(self,
                 name="entity",
                 description="You",
                 x=0,
                 y=0,
                 faction="player",
                 mind=None,
                 body=Body,
                 char="@",
                 colour=tcod.white,
                 blocks=True,
                 area=None):
        super().__init__(name, description, x, y, faction, mind, body,
                         char, colour, blocks, area)

    def take_action(self, instruction):
        """Takes an action based on player input."""

        # If the instruction has a direction
        if isinstance(instruction, Surge):

            # Intepret the action based on area context
            self.interpret_surge(instruction)

        # If the instruction concerns an item
        elif isinstance(instruction, Handle):

            # Interpret the action
            self.interpret_handle(instruction)

        elif isinstance(instruction, OpenInventory):
            self.open_inventory()

        elif isinstance(instruction, OpenMenu):
            self.open_menu()

        elif isinstance(instruction, Look):
            self.look()

        elif isinstance(instruction, Wait):
            self.wait()

    def interpret_surge(self, instruction):
        """Interprets an action with a direction based on context."""

        # Get the target coordinates
        target_x = self.x + instruction.dx
        target_y = self.y + instruction.dy

        # If the target is valid
        if self.area.in_bounds(target_x, target_y):

            # Check for an entity at the target location
            occupant = self.area.get_blocker_at_location(target_x, target_y)

            # If there is an occupant
            if occupant:
                self.attack(occupant)

            # If it's free
            elif self.area.is_free(target_x, target_y):
                # Make a move
                self.move(instruction.dx, instruction.dy)

        # Invalid surge
        else:
            raise Impossible("There is no path that way.")

    def interpret_handle(self, instruction):
        """Choose what to do with an item-related action."""

        # If an item has been specified,
        if instruction.item:

            if isinstance(instruction, PickUp):
                self.pick_up(instruction.item)

            elif isinstance(instruction, Drop):
                self.drop(instruction.item)

            elif isinstance(instruction, Use):
                self.use(instruction.item)

            elif isinstance(instruction, Equip):
                self.equip(instruction.item)

            elif isinstance(instruction, Unequip):
                self.unequip(instruction.item)

            elif isinstance(instruction, Throw):
                self.throw(instruction.item, instruction.target)

        # If no item has been named,
        else:

            if isinstance(instruction, PickUp):

                # Choose an item
                self.select_item_to_pick_up()

    def die(self):
        # Removes the entity from the game, replacing it with a corpse.
        # As this is the player, also ends the game

        super().die()

        self.area.world.engine.game_over()

    def pick_up(self, item):
        """Adds an item to the inventory."""

        text = f"You pick up the {item.name}."
        self.area.post_message(Message(text))

        super().pick_up(item)

    def drop(self, item):
        """Removes an item from the inventory and adds it to the area."""

        text = f"You discard the {item.name}."
        self.area.post_message(Message(text))

        super().drop(item)

    def equip(self, item):
        """Equips an item, unequipping any item of the same type."""

        self.area.post_message(Message(f"You equip the {item.name}."))

        super().equip(item)

    def unequip(self, item):
        """Unequip an item."""
        self.area.post_message(Message(f"You unequip the {item.name}."))

        super().unequip(item)

    def use(self, item):
        """Uses an item on the entity."""
        self.area.post_message(Message(f"You use the {item.name}."))

        super().use(item)

    def open_inventory(self):
        """Open the inventory."""

        # If the inventory is blank, ignore it
        if len(self.inventory) <= 0:
            raise Impossible("You are not carrying anything.")

        # REFACTOR TARGET
        state = InventoryMenu(self.area.world.engine,
                              self.area.world.engine.state,
                              self.inventory)
        self.area.world.engine.set_state(state)

    def look(self):
        """Look around the area."""

        state = LookState(self.area.world.engine, self.area.world.engine.state)
        self.area.world.engine.set_state(state)

    def throw(self, item, target):
        """Throw an object towards a location."""

        text = f"You throw the {item.name}."
        self.area.post_message(Message(text))

        super().throw(item, target)

    def open_menu(self):
        """View the in-game menu."""

        state = InGameMenu(self.area.world.engine,
                           self.area.world.engine.state)
        self.area.world.engine.set_state(state)

    def select_item_to_pick_up(self):
        """Choose an item from the current tile to select."""

        # Get the set of items on the current tile
        contents = self.area.items_at_location(self.x, self.y)

        # If there are any items and there is inventory space:
        if contents and not self.inventory_full:

            # If only one item is present,
            if len(contents) == 1:

                # Grab it
                item = contents.pop()
                self.pick_up(item)

            # If there's more than one item,
            else:

                # Open the selection menu.
                # REFACTOR TARGET
                state = ItemSelectionMenu(self.area.world.engine,
                                          self.area.world.engine.state,
                                          contents)
                self.area.world.engine.set_state(state)

        elif contents:
            raise Impossible("You are carrying too much.")
        else:
            raise Impossible("Nothing to pick up.")
