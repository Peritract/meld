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
        self.options = [MenuOption("Main Menu"),
                        MenuOption("Credits"),
                        MenuOption("Quit", self.quit)]
        self.menu = Menu(self.options)

    def quit(self):
        """Quit the game."""
        raise SystemExit()
