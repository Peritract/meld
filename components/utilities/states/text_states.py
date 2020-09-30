"""This file contains the implementation of several game states that are used
primarily to display text to the user. These aren't menus, just informational.
"""

from .state import State
from textwrap import wrap
from .main_menu_state import MainMenu
from ..constants import COLOURS as C
import tcod


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
                           bg=C["BLACK"], fg=C["WHITE"])

        # Write out the text
        for line in self.lines:
            if line != "BLANK":
                console.print(x + 2, y + 2, line, C["WHITE"])
            y += 1


class MessageScroller(State):
    """Display the message log in a scrolling window."""

    def __init__(self, engine, parent):
        super().__init__(engine)
        self.parent = parent
        self.width = 60
        self.height = 10
        self.messages = self.get_messages()
        self.cursor = len(self.messages) if len(self.messages) <= self.height else len(self.messages) - self.height

    def get_messages(self):
        """Get the list of messages wrapped to the width."""
        messages = self.engine.message_log.get_message_lines(False,
                                                             self.width - 4,
                                                             -1)

        return messages

    def ev_keydown(self, event):
        """Take keyboard input."""

        key = event.sym

        if key == tcod.event.K_UP:
            if self.cursor > 0:
                self.cursor -= 1
        elif key == tcod.event.K_DOWN:
            if self.cursor < len(self.messages) - 4:
                self.cursor += 1
        else:
            self.engine.set_state(self.parent)

    def render(self, console):
        """Display the messages over the parent state."""

        # Show the parent
        self.parent.render(console)

        # Calculate the starting y
        # halfway point - half height
        y = self.engine.screen_height // 2 - self.height // 2

        # Calculate the starting x
        # half way point - half width
        x = self.engine.screen_width // 2 - self.width // 2

        # Draw a black panel as a frame
        console.draw_frame(x, y, self.width, self.height,
                           bg=C["BLACK"], fg=C["WHITE"])

        # Display the messages
        self.render_messages(console, x, y)

    def render_messages(self, console, x, y):
        """Display a list of messages."""

        offset = 2
        print(self.cursor)

        # Loop through the messages,
        for message in self.messages[self.cursor:]:
            # Display the message
            console.print(x + 2, y + offset, message[0], message[1])

            # Up the offset
            offset += 1

            # Don't draw off the page
            if offset >= self.height - 2:
                return
