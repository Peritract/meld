"""
This file contains the implementation of the MainMenu class.
This class begins the game and presents the player with options.
"""

from .menus import MenuOption, Menu


class MainMenu(Menu):

    def __init__(self, engine):
        super().__init__(engine)

        # Set the options
        self.options = [MenuOption("Start New Game",
                                   self.engine.new_game),
                        MenuOption("Continue Game",
                                   self.engine.load_game),
                        MenuOption("Quit Game", self.quit)]
