"""This file contains the implementation of the InventoryMenu class;
This shows the player their current inventory and allows them to manipulate it.
"""

from .overlay_menu import OverlayMenu
from .menu import MenuOption
from ..constants import colours as C
from ...entities.actions import Drop, Use, Equip, Unequip
import tcod


class InventoryOption(MenuOption):
    """A menu option for the inventory,
    with multiple control responses."""

    def __init__(self, item):
        super().__init__(self, item)
        self.item = item
        self.name = item.name
        self.drop = Drop(item)
        self.use = Use(item) if item.usable else None
        self.equip = Equip(item) if item.equippable else None
        self.unequip = Unequip(item) if item.equippable else None


class InventoryMenu(OverlayMenu):
    """Displays the current inventory."""

    def __init__(self, engine, parent, items):
        super().__init__(engine, parent)
        self.items = items
        self.options = self.parse_items()

    def parse_items(self):
        """Converts a set of items into menu options."""
        return [InventoryOption(x) for x in self.items]

    def drop(self):
        """Choose to drop an item."""
        self.resume_with_choice(self.selected.drop)

    def use(self):
        """Choose to use an item."""

        if self.selected.use:
            self.resume_with_choice(self.selected.use)

    def process_equip(self):
        """Handle equip commands based on context."""
        if self.selected.equip and self.selected.item.equipped:
            self.unequip()
        elif self.selected.equip and not self.selected.item.equipped:
            self.equip()

    def equip(self):
        """Choose to equip an item."""
        self.resume_with_choice(self.selected.equip)

    def unequip(self):
        """Choose to unequip an item."""
        self.resume_with_choice(self.selected.unequip)

    def resume_with_choice(self, option):
        """Return control to the parent state, passing back a decision."""

        # Return to the previous state
        self.resume()

        # Pass an action to be handled
        self.engine.state.handle_event(option)

    def ev_keydown(self, event):
        """Take keyboard input."""

        # Get event information
        key = event.sym

        if key == tcod.event.K_UP:
            self.change_selection(-1)

        elif key == tcod.event.K_DOWN:
            self.change_selection(1)

        elif key == tcod.event.K_ESCAPE or key == tcod.event.K_i:
            self.resume()

        elif key == tcod.event.K_d:
            self.drop()

        elif key == tcod.event.K_u:
            self.use()

        elif key == tcod.event.K_e:
            self.process_equip()

    def render_overlay(self, console):
        """Renders the menu options over the rest of the screen."""

        # Calculate the starting y
        # halfway point - half height
        offset = self.engine.screen_height // 2 - self.height // 2

        # Calculate the starting x
        # half way point - half width
        x_start = self.engine.screen_width // 2 - self.width // 2

        console.draw_frame(x_start, offset, self.width, self.height)

        for option in self.options:
            colour = C["GOLD"] if option == self.selected else C["WHITE"]
            text = self.wrapped_text(option.name)

            # Start text one in and two down
            console.print(x_start + 1, offset + 2, text, colour)

            # Leave a gap between each line
            offset += 2
