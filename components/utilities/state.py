"""
This class contains the implementation of the base State class.
"""

import tcod
import traceback


class State(tcod.event.EventDispatch):
    """A game state."""

    def __init__(self, engine):
        self.engine = engine

    def render(self, console):
        """Display all relevant information."""
        pass

    def handle_events(self, window):
        """Handles in-game input events."""

        try:
            # Check for events
            for event in tcod.event.wait():

                # Extract mouse location details
                window.convert_event(event)

                # Pass the event to handlers
                self.handle_event(self.dispatch(event))

        except Exception:
            print(traceback.format_exc())

    def handle_event(self, action):
        """React to a valid input."""
        pass

    def ev_quit(self, event):
        """Exit the program."""
        raise SystemExit()

    def ev_mousemotion(self, event):
        """Log mouse movement."""
        self.engine.m_loc = (event.tile.x, event.tile.y)
