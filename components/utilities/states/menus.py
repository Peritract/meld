"""This file contains the necessary classes for creating
and displaying menus."""

from ..constants import COLOURS as C
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

        console.draw_frame(x_start, offset, self.width, self.height,
                           bg=C["BLACK"], fg=C["WHITE"])

        for option in self.options:
            colour = C["GOLD"] if option == self.selected else C["WHITE"]
            text = self.wrap_text(option.name)

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

    def wrap_text(self, text):
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


class OverlayMenu(Menu):
    """A menu that renders a panel over another game state."""

    def __init__(self, engine, parent, center=True):
        super().__init__(engine)
        self.parent = parent
        self.center = center

    def render(self, console):

        # Render the parent
        self.parent.render(console)

        # Render the overlay menu
        self.render_overlay(console)

    def resume(self):
        """Return control to the parent state."""

        self.engine.set_state(self.parent)

    def resume_with_choice(self):
        """Return control to the parent state, passing back a decision."""

        # Return to the previous state
        self.resume()

        # Pass an action to be handled
        self.engine.state.handle_event(self.selected.value)

    def ev_keydown(self, event):
        """Take keyboard input."""

        # Get event information
        key = event.sym

        if key == tcod.event.K_UP:
            self.change_selection(-1)

        elif key == tcod.event.K_DOWN:
            self.change_selection(1)

        elif key == tcod.event.K_RETURN:
            self.process_option()

        elif key == tcod.event.K_ESCAPE:
            self.resume()

    def process_option(self):
        """Decide how to respond to the selected option."""

        # If the option has a value
        if self.selected.value:

            # End the menu and pass back the value to the parent state
            self.resume_with_choice()

        # If it's just a method,
        else:

            # Call it
            self.select_option()

    def render_overlay(self, console):
        """Renders the menu options over the rest of the screen."""

        # Calculate the starting y
        # halfway point - half height
        offset = self.engine.screen_height // 2 - self.height // 2

        # Calculate the starting x
        # half way point - half width
        x_start = self.engine.screen_width // 2 - self.width // 2

        console.draw_frame(x_start, offset, self.width, self.height,
                           bg=C["BLACK"], fg=C["WHITE"])

        for option in self.options:
            colour = C["GOLD"] if option == self.selected else C["WHITE"]
            text = self.wrap_text(option.name) if self.center else option.name

            # Start text one in and two down
            console.print(x_start + 1, offset + 2, text, colour)

            # Leave a gap between each line
            offset += 2
