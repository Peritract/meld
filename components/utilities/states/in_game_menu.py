"""This file contains the implementation of the InGameMenu class.
This is the menu that appears when the player presses ESC in-game.
"""

from .overlay_menu import OverlayMenu
# from ..states.main_menu_state import MainMenu
from .menu import MenuOption
from ..constants import COLOURS as C
import lzma
import pickle


class InGameMenu(OverlayMenu):
    """Present the user with game options."""

    def __init__(self, engine, parent):
        super().__init__(engine, parent)

        self.options = [MenuOption("Resume", self.resume),
                        MenuOption("Save & Quit", self.save),
                        MenuOption("Quit Without Saving", self.quit)]

    def save(self):
        """Save the game to a file and return to the main menu."""
        data = lzma.compress(pickle.dumps(self.engine.world))
        with open("savegame.sav", "wb") as file:
            file.write(data)

        self.engine.set_state(MainMenu(self.engine))

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
