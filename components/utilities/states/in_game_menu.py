"""This file contains the implementation of the InGameMenu class.
This is the menu that appears when the player presses ESC in-game.
"""

from .overlay_menu import OverlayMenu
from .menu import MenuOption
from ..constants import COLOURS as C


class InGameMenu(OverlayMenu):
    """Present the user with game options."""

    def __init__(self, engine, parent):
        super().__init__(engine, parent)

        self.options = [MenuOption("Resume", self.resume),
                        MenuOption("Quit Game", self.quit)]

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
            text = self.wrap_text(option.name)

            # Start text one in and two down
            console.print(x_start + 1, offset + 2, text, colour)

            # Leave a gap between each line
            offset += 2
