"""
This file contains the implementation of the GameOverState class.
This class wraps everything up and presents the player with
the only valid options.
"""

from .state import State
from .constants import colours as C
from .menu import MenuOption
import tcod


class GameOverState(State):

    def __init__(self, engine):
        super().__init__(engine)
        self.selection = 0
        self.options = [MenuOption("Main Menu"),
                        MenuOption("Credits"),
                        MenuOption("Quit", self.quit)]

    @property
    def selected(self):
        """Returns the currently-selected option."""
        return self.options[self.selection]

    def render(self, console):

        offset = 15

        for option in self.options:
            colour = C["GOLD"] if option == self.selected else C["WHITE"]
            console.print(15, offset, option.name, colour)
            offset += 2

    def change_selection(self, value):
        """Change the selection"""
        self.selection += value
        if self.selection < 0:
            self.selection = len(self.options) - 1
        elif self.selection >= len(self.options):
            self.selection = 0

    def select_option(self):
        """Act on the selected option."""
        if self.selected.method:
            self.selected.method()

    def quit(self):
        """Quit the game."""
        raise SystemExit()

    def ev_keydown(self, event):
        """Take keyboard input."""

        # Get event information
        key = event.sym

        if key == tcod.event.K_ESCAPE:
            print("QUITTING!")

        elif key == tcod.event.K_UP:
            self.change_selection(-1)

        elif key == tcod.event.K_DOWN:
            self.change_selection(1)

        elif key == tcod.event.K_RETURN:
            self.select_option()
