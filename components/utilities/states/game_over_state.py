"""
This file contains the implementation of the GameOverState class.
This class wraps everything up and presents the player with
the only valid options.
"""

from .menu import MenuOption, Menu


class GameOverState(Menu):

    def __init__(self, engine):
        super().__init__(engine)

        # Set the options
        self.options = [MenuOption("Main Menu", self.change_state_to_main),
                        MenuOption("Credits"),
                        MenuOption("Quit Game", self.quit)]

    def quit(self):
        """Quit the game."""
        raise SystemExit()

    def change_state_to_main(self):
        """Changes the game state to the main menu."""
        self.engine.set_state("main_menu")
