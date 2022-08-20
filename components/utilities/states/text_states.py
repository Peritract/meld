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
                "\nTom Keefe\nTyler Standridge.")

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
        self.width = 50
        self.height = 50
        self.messages = self.get_messages()

        # if there are fewer messages than fill the screen, start at zero
        if len(self.messages) < self.height - 4:
            self.cursor = 0
        # Otherwise
        else:
            # Start the cursor so the latest message is the last line
            self.cursor = len(self.messages) - (self.height - 4)

    def get_messages(self):
        """Get the list of messages wrapped to the width."""
        messages = self.engine.message_log.get_message_lines(False,
                                                             self.width - 4,
                                                             -1)
        return messages

    def ev_keydown(self, event):
        """Take keyboard input."""

        key = event.sym
        # Move faster with shift
        mod = 5 if event.mod == 1 else 1

        if key == tcod.event.K_UP:
            if self.cursor > 0:
                self.cursor = max([0, self.cursor - 1 * mod])
        elif key == tcod.event.K_DOWN:
            if self.cursor < len(self.messages) - (self.height - 4):
                self.cursor = min([self.cursor + 1 * mod,
                                   len(self.messages) - (self.height - 4)])
        elif key == tcod.event.K_ESCAPE or key == tcod.event.K_RETURN:
            self.engine.set_state(self.parent)

    def ev_mousebuttondown(self, event):
        """Selects on mouse click."""
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

        # Get the messages that need displaying
        to_display = self.messages[self.cursor:]

        offset = 2

        for message in to_display:
            console.print(x + 2, y + offset, message[0], message[1])
            offset += 1

            if offset >= self.height - 2:
                return


class DescriptionScroller(State):
    """Allows the user to scroll through descriptions;
       this state overlays on top of another one."""

    def __init__(self, engine, parent, objects):
        super().__init__(engine)
        self.parent = parent
        self.objects = objects
        self.cursor = 0
        self.height = 10
        self.width = 20

    def render(self, console):
        """Render one description on a panel."""

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

        # Get the current object to describe
        obj = self.objects[self.cursor]

        # Display the object name
        console.print(x + 2, y + 2, obj.name, obj.colour)

        # Leave a line, and display the description
        lines = wrap(obj.description, self.width - 4)
        offset = 4

        for line in lines:
            console.print(x + 2, y + offset, line, C["WHITE"])
            offset += 1

        # Display controls at the bottom right of the panel
        left_cursor = C["WHITE"] if self.cursor > 0 else C["GREY"]
        right_cursor = C["WHITE"] if self.cursor < len(self.objects) - 1 \
            else C["GREY"]
        console.print(x + (self.width - 4), y + (self.height - 2),
                      "<", left_cursor)
        console.print(x + (self.width - 2), y + (self.height - 2),
                      ">", right_cursor)

    def ev_keydown(self, event):
        """Take keyboard input."""

        key = event.sym

        if key == tcod.event.K_LEFT:
            if self.cursor > 0:
                self.cursor -= 1
        elif key == tcod.event.K_RIGHT:
            if self.cursor < len(self.objects) - 1:
                self.cursor += 1
        else:
            self.engine.set_state(self.parent)
