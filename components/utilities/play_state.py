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
            action = self.dispatch(event)

            # If no action has been chosen, pass on
            if not action:
                continue

            # Pass the action to the player
            self.engine.player.take_action(action)

            # Let all other entities take turns
            for entity in self.engine.world.entities - {self.engine.player}:
                entity.take_action()

    def render(self, console):
        """Display the current state of the game world."""

        # Show all the entities
        for entity in self.engine.world.entities:
            console.print(entity.x, entity.y, entity.char, entity.colour)

        # If the mouse is over a tile
        if self.engine.world.area.in_bounds(*self.engine.m_loc):

            # Get the tile contents
            contents = self.engine.world.area.at_location(*self.engine.m_loc)

            if contents:
                contents_string = " ".join([thing.name for thing in contents])
                console.print(20, 20, contents_string)
