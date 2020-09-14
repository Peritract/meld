"""
This file contains the implementation of the MainMenuState class.
This class begins the game and presents the player with options.
"""

from .menu import MenuOption, Menu


class MainMenuState(Menu):

    def __init__(self, engine):
        super().__init__(engine)

        # Set the options
        self.options = [MenuOption("Start New Game",
                                   self.change_state_to_new),
                        MenuOption("Quit Game", self.quit)]

    def quit(self):
        """Quit the game."""
        raise SystemExit()

    def change_state_to_new(self):
        """Changes the game state to the main menu."""
        self.engine.set_state("new_game")
