"""This file contains the necessary classes for creating
and displaying menus."""

from .constants import colours as C
from .state import State
import tcod


class MenuOption:
    """A single menu option."""

    def __init__(self, name="Option", method=None):
        self.name = name
        self.method = method


class Menu(State):

    def __init__(self, engine):
        super().__init__(engine)
        self.selection = 0

        # Default to no options
        self.options = None

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
