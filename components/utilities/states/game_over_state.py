"""
This file contains the implementation of the GameOverState class.
This class wraps everything up and presents the player with
the only valid options.
"""

from .menus import OverlayMenu, MenuOption
from .main_menu_state import MainMenu
from .text_state import Credits
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
