"""
This file contains the implementation of the PlayState class.
This is the "game" bit - it manages turn-taking and level/unit display.
"""

from ..entities.actions import Surge, Wait
from .state import State

import tcod


class PlayState(State):
    """Manages game turns and display."""

    def __init__(self, engine):
        super().__init__(engine)

    def ev_keydown(self, event):
        """Take keyboard input."""

        # Get event information
        key = event.sym

        # Default to None
        action = None

        # Movement keys
        if key == tcod.event.K_UP:
            action = Surge(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = Surge(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = Surge(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = Surge(dx=1, dy=0)
        elif key == tcod.event.K_PERIOD:
            action = Wait()

        return action

    def handle_events(self, window):
        """Handles in-game events."""

        # Check for events
        for event in tcod.event.wait():

            # Extract mouse location details
            window.convert_event(event)

            # Pass the event to handlers
            self.dispatch(event)

    def render(self, console):
        for entity in self.engine.world.current_area.entities:
            console.print(entity.x, entity.y, entity.char)
