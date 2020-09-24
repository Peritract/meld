"""
This file contains the implementation of the GameOverState class.
This class wraps everything up and presents the player with
the only valid options.
"""

from .overlay_menu import OverlayMenu
from .menu import MenuOption
from .main_menu_state import MainMenu
from .text_state import Credits
from ...utilities.constants import COLOURS as C
import tcod


class GameOver(OverlayMenu):

    def __init__(self, engine, parent):
        super().__init__(engine, parent)

        # Set the options
        self.options = [MenuOption("Main Menu", self.show_main_menu),
                        MenuOption("Credits", self.show_credits),
                        MenuOption("Quit Game", self.quit)]

    def show_main_menu(self):
        """Changes the game state to the main menu."""
        self.engine.set_state(MainMenu(self.engine))

    def show_credits(self):
        """Change the game state to show the credits."""
        self.engine.set_state(Credits(self.engine))

    def render_overlay(self, console):
        """Renders the menu options over the rest of the screen."""

        # Calculate the starting y
        # halfway point - half height
        offset = self.engine.screen_height // 2 - self.height // 2

        # Calculate the starting x
        # half way point - half width
        x_start = self.engine.screen_width // 2 - self.width // 2

        console.draw_frame(x_start, offset, self.width, self.height,
                           bg=C["BLACK"])

        for option in self.options:
            colour = C["GOLD"] if option == self.selected else C["WHITE"]
            text = self.wrap_text(option.name)

            # Start text one in and two down
            console.print(x_start + 1, offset + 2, text, colour)

            # Leave a gap between each line
            offset += 2

    def ev_keydown(self, event):
        """Take keyboard input."""

        # Get event information
        key = event.sym

        if key == tcod.event.K_UP:
            self.change_selection(-1)

        elif key == tcod.event.K_DOWN:
            self.change_selection(1)

        elif key == tcod.event.K_RETURN:
            self.process_option()
