"""This file contains the implementation of the TextState class
and its subclasses. This class displays text for the player and
is dismissed on input.
"""

from .state import State
from ..message_log import Message
from ..constants import colours as C
from .main_menu_state import MainMenuState


class TextState(State):
    """Displays text and dismisses on keyboard input."""
    def __init__(self, engine, target, lines):
        super().__init__(engine)

        # The state to be returned to
        self.target = target

        # The lines of text to display
        self.lines = lines

    @property
    def height(self):
        return len(self.lines)

    @property
    def width(self):
        return max([len(x.text) for x in self.lines])

    def wrap_text(self, text):
        """Return a centered string based on the menu width."""

        # Subtract 2 for the margins
        return text.center(self.width - 2)

    def ev_keydown(self, event):
        """Take keyboard input."""
        self.engine.set_state(self.target)

    def render(self, console):
        """Display the text."""

        # Calculate the starting y
        # halfway point - half height
        y = self.engine.screen_height // 2 - self.height // 2

        # Calculate the starting x
        # half way point - half width
        x = self.engine.screen_width // 2 - self.width // 2

        # Display each line
        for line in self.lines:
            console.print(x, y, self.wrap_text(line.text), line.colour)
            y += 1


class Credits(TextState):
    """The game credits."""

    def __init__(self, engine):

        lines = [Message("Designed & created by", C["WHITE"]),
                 Message("", C["TEMP"]),
                 Message("Dan Keefe", C["WHITE"]),
                 Message("", C["TEMP"]),
                 Message("Special thanks to:", C["WHITE"]),
                 Message("", C["TEMP"]),
                 Message("Tom Keefe", C["WHITE"]),
                 Message("Tyler Standridge", C["WHITE"]),
                 Message("", C["TEMP"]),
                 Message("", C["TEMP"]),
                 Message("Press any key to return to the main menu",
                         C["GOLD"])]

        super().__init__(engine, MainMenuState(engine), lines)
