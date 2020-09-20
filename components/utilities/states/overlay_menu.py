"""This file contains the implementation of the OverlayMenu class.
This is a game state that draws a menu over the display of another state.
"""

from .menu import Menu
import tcod


class OverlayMenu(Menu):

    def __init__(self, engine, parent):
        super().__init__(engine)
        self.parent = parent

    def render(self, console):

        # Render the parent
        self.parent.render(console)

        # Render the overlay menu
        self.render_overlay(console)

    def render_overlay(self, console):
        """Display a menu over another state."""
        raise NotImplementedError()

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
