"""This file contains the implementation of the InGameMenu class.
This is the menu that appears when the player presses ESC in-game.
"""

from .menus import OverlayMenu, MenuOption


class InGameMenu(OverlayMenu):
    """Present the user with game options."""

    def __init__(self, engine, parent):
        super().__init__(engine, parent)

        self.options = [MenuOption("Resume", self.resume),
                        MenuOption("Save & Quit", self.save),
                        MenuOption("Quit Without Saving", self.quit)]

    def save(self):
        """Save the game to a file and return to the main menu."""
        self.engine.save_game()
