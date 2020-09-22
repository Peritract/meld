"""
This file contains the implementation of the MainMenu class.
This class begins the game and presents the player with options.
"""

from .menu import MenuOption, Menu
from .new_game_state import NewGame
from .load_game_state import LoadGame


class MainMenu(Menu):

    def __init__(self, engine):
        super().__init__(engine)

        # Set the options
        self.options = [MenuOption("Start New Game",
                                   self.start_new_game),
                        MenuOption("Continue Game",
                                   self.load_game),
                        MenuOption("Quit Game", self.quit)]

    def start_new_game(self):
        """Changes the game state to the main menu."""
        self.engine.set_state(NewGame(self.engine))

    def load_game(self):
        """Changes the game state to the loading state."""
        self.engine.set_state(LoadGame(self.engine))
