"""This file contains the implementation of the OverlayMenu class.
This is a game state that draws a menu over the display of another state.
"""

from .menu import Menu


class OverlayMenu(Menu):

    def __init__(self, engine, parent_state):
        super().__init__(engine)
        self.parent = parent_state

    def render(self, console):

        # Render the parent
        self.parent.render(console)

        # Render the overlay menu
        self.render_overlay(console)

    def render_overlay(self, console):
        """Display a menu over another state."""
        pass

    def remove_overlay(self):
        """Return control to the parent state."""

        self.engine.set_state(self.parent)