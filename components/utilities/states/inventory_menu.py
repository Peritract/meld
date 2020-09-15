"""This file contains the implementation of the InventoryMenu class;
This shows the player their current inventory and allows them to manipulate it.
"""

from .overlay_menu import OverlayMenu
from .menu import MenuOption
from ..constants import colours as C
from ...entities.actions import Drop


class InventoryMenu(OverlayMenu):
    """Displays the current inventory."""

    def __init__(self, engine, parent, items):
        super().__init__(engine, parent)
        self.items = items
        self.options = self.parse_items()

    def parse_items(self):
        """Converts a set of items into menu options."""
        return [MenuOption(x.name, value=Drop(x)) for x in self.items]

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
