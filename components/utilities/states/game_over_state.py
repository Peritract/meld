"""
This file contains the implementation of the GameOverState class.
This class wraps everything up and presents the player with
the only valid options.
"""

from .menu import MenuOption, Menu
from .main_menu_state import MainMenuState
from .text_state import Credits


class GameOverState(Menu):

    def __init__(self, engine):
        super().__init__(engine)

        # Set the options
        self.options = [MenuOption("Main Menu", self.show_main_menu),
                        MenuOption("Credits", self.show_credits),
                        MenuOption("Quit Game", self.quit)]

    def show_main_menu(self):
        """Changes the game state to the main menu."""
        self.engine.set_state(MainMenuState(self.engine))

    def show_credits(self):
        """Change the game state to show the credits."""
        self.engine.set_state(Credits(self.engine))
