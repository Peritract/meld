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

        # Display the info bar
        self.render_info_pane(console, 20, 20)

        # Display the status pane
        self.render_status_pane(console, 30, 30)

    # Utility rendering functions

    def render_info_pane(self, console, x, y):
        """Displays information about the tile under the mouse."""

        # If the mouse is over a tile
        if self.engine.world.area.in_bounds(*self.engine.m_loc):

            # Get the tile contents
            contents = self.engine.world.area.at_location(*self.engine.m_loc)

            # If there is anything to display
            if contents:
                # Display it
                contents_string = " ".join([thing.name for thing in contents])
                console.print(x, y, contents_string)

    def render_status_pane(self, console, x, y):
        """Displays a status panel with key information about
           the area & player."""

        # Show key details
        console.print(x, y, self.engine.world.area.name, tcod.white)

        # Show the health bar
        self.render_bar(console, x, y + 1, 30,
                        self.engine.player.body.health,
                        self.engine.player.body.max_health,
                        tcod.dark_gray, tcod.dark_green, "Health",
                        tcod.white)

    def render_bar(self, console, x, y, max_width,
                   value=0, max_value=10,
                   background_colour=tcod.dark_gray,
                   colour=tcod.dark_blue,
                   caption="", caption_colour=tcod.white):
        """Renders a stat bar with a numeric overlay."""

        # Calculate the width
        width = int(value / max_value * max_width)

        # Display the background
        console.draw_rect(x, y, max_width, 1, 1, bg=background_colour)

        # If there's anything on the bar
        if width > 0:
            # Draw the bar over the top
            console.draw_rect(x, y, width, 1, 1, bg=colour)

        # Put the numbers over the top
        console.print(x, y, f"{caption}: {value}/{max_value}", caption_colour)
