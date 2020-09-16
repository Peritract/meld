"""
This file contains the implementation of the Player class.
This is the game's player character.
"""

from .entity import Entity
from .actions import (Surge, Move, Attack, Wait, PickUp, OpenInventory,
                      Drop, Use)
from ..items.corpse import Corpse
from ..utilities.message_log import Message
from ..entities.body import Body
from ..utilities.exceptions import Impossible
from ..utilities.states.item_selection_menu import ItemSelectionMenu
from ..utilities.states.inventory_menu import InventoryMenu

import tcod


class Player(Entity):
    """The player character."""

    def __init__(self,
                 name="entity",
                 x=0,
                 y=0,
                 faction="player",
                 mind=None,
                 body=Body,
                 char="@",
                 colour=tcod.white,
                 blocks=True,
                 area=None):
        super().__init__(name, x, y, faction, mind, body,
                         char, colour, blocks, area)

    def take_action(self, instruction):
        """Takes an action based on player input."""

        # If the instruction has a direction
        if isinstance(instruction, Surge):

            # Intepret the action based on area context
            action = self.interpret_surge(instruction)

            # Act on the interpretation
            if isinstance(action, Move):
                self.move(action.dx, action.dy)
            elif isinstance(action, Attack):
                self.attack(action.other)

        elif isinstance(instruction, PickUp):

            # If there's an item already,
            if instruction.item:

                # Pick it up
                self.pick_up(instruction.item)

            # otherwise,
            else:
                # Choose one
                self.select_item_to_pick_up()

        elif isinstance(instruction, Drop):

            # Check that an object has been referred to.
            if instruction.item:
                self.drop(instruction.item)

        elif isinstance(instruction, Use):

            # Check that an object has been referred to.
            if instruction.item:
                self.use(instruction.item)

        elif isinstance(instruction, OpenInventory):
            self.open_inventory()

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
                return Attack(occupant)

            # If it's free
            if self.area.is_free(target_x, target_y):
                # Make a move
                return Move(instruction.dx, instruction.dy)

        # Invalid surge
        raise Impossible("There is no path that way.")

    def die(self):
        # Removes the entity from the game, replacing it with a corpse.
        # As this is the player, also ends the game
        self.area.contents.remove(self)
        self.area.contents.add(Corpse(self.name, self.x, self.y))
        self.area.post_message(Message(f"The {self.name} dies in agony."))
        self.area.world.engine.game_over()

    def pick_up(self, item):
        """Adds an item to the inventory."""
        self.inventory.add(item)
        self.area.contents.remove(item)
        text = f"You pick up the {item.name}."
        self.area.post_message(Message(text))

    def drop(self, item):
        """Removes an item from the inventory and adds it to the area."""
        self.inventory.remove(item)

        # Place it in the current tile
        item.x, item.y = self.x, self.y

        self.area.contents.add(item)
        text = f"You discard the {item.name}."
        self.area.post_message(Message(text))

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
