"""This file contains the implementation of the InventoryMenu class;
This shows the player their current inventory and allows them to manipulate it.
"""

from .overlay_menu import OverlayMenu
from .menu import MenuOption
from ..constants import COLOURS as C
from ...entities.actions import Drop, Use, Equip, Unequip
from ...items.items import Consumable, Equippable
import tcod
from textwrap import wrap
from .throw_state import ThrowState


class InventoryOption(MenuOption):
    """A menu option for the inventory,
    with multiple control responses."""

    def __init__(self, item):
        super().__init__(self, item)
        self.item = item
        self.drop = Drop(item)
        self.use = Use(item) if isinstance(item, Consumable) else None
        self.equip = Equip(item) if isinstance(item, Equippable) else None
        self.unequip = Unequip(item) if isinstance(item, Equippable) else None

    @property
    def display_text(self):
        """Get the text to display."""

        if isinstance(self.item, Equippable) and self.item.equipped:
            return self.item.name + " E"

        return self.item.name


class InventoryMenu(OverlayMenu):
    """Displays the current inventory."""

    def __init__(self, engine, parent, items):
        super().__init__(engine, parent)
        self.items = self.order_items(items)
        self.options = self.parse_items()

    @property
    def width(self):
        """Returns the (set) width of the inventory window."""
        return 41

    @property
    def height(self):
        """Returns the (variable) height of the inventory window."""
        return len(self.items) * 2 + 6

    def parse_items(self):
        """Converts a set of items into menu options."""
        return [InventoryOption(x) for x in self.items]

    def drop(self):
        """Choose to drop an item."""
        self.resume_with_choice(self.selected.drop)

    def plan_throw(self):
        """Select where to throw an item."""

        # Change the state to the targetting one
        # Pass in the play state underneath - done with this menu
        self.engine.state = ThrowState(self.engine,
                                       self.parent,
                                       self.selected.item)

    def use(self):
        """Choose to use an item."""
        self.resume_with_choice(self.selected.use)

    def process_equip(self):
        """Handle equip commands based on context."""
        if self.selected.item.equipped:
            self.unequip()
        else:
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

        elif key == tcod.event.K_t:
            self.plan_throw()

        elif key == tcod.event.K_u:
            if isinstance(self.selected.item, Consumable):
                self.use()

        elif key == tcod.event.K_e:
            if isinstance(self.selected.item, Equippable):
                self.process_equip()

    def order_items(self, items):
        """Order the items alphabetically with equipped items first."""
        return sorted(sorted(items, key=lambda x: x.name),
                      key=lambda x: isinstance(x, Equippable) and x.equipped,
                      reverse=True)

    # Rendering methods

    def render_controls(self, x, y, console):
        """Displays the appropriate controls of the current item."""
        if self.selected.use:
            console.print(x, y, "[U]se", C["WHITE"])
        else:
            console.print(x, y, "[U]se", C["GREY"])
        x += 6

        if self.selected.equip and not self.selected.item.equipped:
            console.print(x, y, "[E]quip", C["WHITE"])
        else:
            console.print(x, y, "[E]quip", C["GREY"])
        x += 8

        if self.selected.equip and self.selected.item.equipped:
            console.print(x, y, "Un[E]quip", C["WHITE"])
        else:
            console.print(x, y, "Un[E]quip", C["GREY"])
        x += 10

        # Throw and drop are always options

        console.print(x, y, "[T]hrow", C["WHITE"])

        x += 8

        console.print(x, y, "[D]rop", C["WHITE"])

    def render_description(self, x, y, console):
        """Render the description of the selected item."""
        lines = wrap(self.selected.item.description_text, 23)
        for line in lines:
            console.print(x, y, line, C["WHITE"])
            y += 1

    def render_overlay(self, console):
        """Renders the menu options over the rest of the screen."""

        # Calculate the starting y
        # halfway point - half height
        offset = self.engine.screen_height // 2 - self.height // 2
        y = offset

        # Calculate the starting x
        # half way point - half width
        x = self.engine.screen_width // 2 - self.width // 2

        console.draw_frame(x, y, self.width, self.height)

        for option in self.options:
            colour = C["GOLD"] if option == self.selected else C["WHITE"]
            text = option.display_text

            # Start text one in and two down
            console.print(x + 1, y + 2, text, colour)

            # Leave a gap between each line
            y += 2

        # Display the appropriate option
        self.render_controls(x + 1, y + 3, console)

        # Render the description of the currently-selected item on the right.
        self.render_description(x + 16, offset + 2, console)
