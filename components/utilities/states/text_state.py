"""This file contains the implementation of the TextState class
and its subclasses. This class displays text for the player and
is dismissed on input.
"""

from .state import State
from textwrap import wrap
from .main_menu_state import MainMenu
from ..constants import COLOURS as C


class TextState(State):
    """Displays text and dismisses on keyboard input."""
    def __init__(self, engine, target, text, center=False):
        super().__init__(engine)
        self.center = center

        # The state to be returned to
        self.target = target

        # The text to display
        self.text = text

        self.lines = self.wrap_text(text)

    @property
    def height(self):
        return len(self.lines) + 4

    @property
    def width(self):
        return min([40, max([len(x) for x in self.text.split("\n")]) + 4])

    def center_text(self, text):
        """Return a centered string based on the menu width."""

        # Subtract 2 for the margins
        return text.center(self.width - 2)

    def wrap_text(self, text):
        """Wrap the text to a given width."""

        # Split lines at \n
        lines = [wrap(x, self.width) for x in text.split("\n")]

        # Flatten lists of lines
        lines = [y for x in lines for y in x]

        # Center text if required
        if self.center:
            lines = [self.center_text(x) for x in lines]

        return lines

    def ev_keydown(self, event):
        """Take keyboard input."""
        self.engine.set_state(self.target)

    def ev_mousebuttondown(self, event):
        """Selects on mouse click."""
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
            console.print(x, y, line, C["WHITE"])
            y += 2


class Credits(TextState):
    """The game credits."""

    def __init__(self, engine):

        text = ("Designed and created by\nDan Keefe.\nSpecial thanks to"
                "\nTom Keefe\nTyle Standridge.")

        super().__init__(engine, MainMenu(engine), text, True)


class OverlayText(TextState):
    """Displays text over another state's rendering."""

    def __init__(self, engine, target, parent, text, center=False):
        super().__init__(engine, target, text, center)
        self.parent = parent

    def render(self, console):
        """Display the text over another menu."""

        self.parent.render(console)

        # Calculate the starting y
        # halfway point - half height
        y = self.engine.screen_height // 2 - self.height // 2

        # Calculate the starting x
        # half way point - half width
        x = self.engine.screen_width // 2 - self.width // 2

        # Draw a black panel as a frame
        console.draw_frame(x, y, self.width, self.height,
                           bg=C["BLACK"])

        # Write out the text
        for line in self.lines:
            if line != "BLANK":
                console.print(x + 2, y + 2, line, C["WHITE"])
            y += 1
