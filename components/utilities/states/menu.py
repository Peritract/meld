"""This file contains the necessary classes for creating
and displaying menus."""

from ..constants import colours as C
from .state import State
import tcod


class MenuOption:
    """A single menu option."""

    def __init__(self, name="Option", method=None, value=None):
        self.name = name
        self.method = method
        self.value = value


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

        # Calculate the starting y
        # halfway point - half height
        offset = self.engine.screen_height // 2 - self.height // 2

        # Calculate the starting x
        # half way point - half width
        x_start = self.engine.screen_width // 2 - self.width // 2

        console.draw_frame(x_start, offset, self.width, self.height)

        for option in self.options:
            colour = C["GOLD"] if option == self.selected else C["WHITE"]
            text = self.wrapped_text(option.name)

            # Start text one in and two down
            console.print(x_start + 1, offset + 2, text, colour)

            # Leave a gap between each line
            offset += 2

    @property
    def width(self):
        """Returns the max width of the menu."""

        if self.options:

            # longest item + 2 for the border + 2 for the margin
            return max([len(x.name) for x in self.options]) + 4

    @property
    def height(self):
        """Returns the max height of the menu."""

        # Two lines per option + 2 for borders + 1 to even out margins
        return len(self.options) * 2 + 2 + 1

    def wrapped_text(self, text):
        """Return a centered string based on the menu width."""

        # Subtract 2 for the margins
        return text.center(self.width - 2)

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

    def quit(self):
        """Quit the game."""
        raise SystemExit()
