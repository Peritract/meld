"""
This file contains the implementation of the PlayState class.
This is the "game" bit - it manages turn-taking and level/unit display.
"""

from ..entities.actions import Surge, Wait
from .state import State
from .constants import directions
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
            action = Surge(*directions["up"])
        elif key == tcod.event.K_DOWN:
            action = Surge(*directions["down"])
        elif key == tcod.event.K_LEFT:
            action = Surge(*directions["left"])
        elif key == tcod.event.K_RIGHT:
            action = Surge(*directions["right"])
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
            self.engine.player.take_action(action, self.engine.world.area)

            # Let all other entities take turns
            for entity in self.engine.world.entities - {self.engine.player}:
                entity.take_action(self.engine.world.area)

    def render(self, console):
        """Display the current state of the game world."""

        # Update tile appearances
        self.engine.world.area.update_tile_states(self.engine.player)

        # Draw the tiles
        self.render_tiles(console)

        # Display the area contents
        self.render_contents(console)

        # Display the status pane
        self.render_status_pane(console, 1, 51, 30)

        # Display the message window
        self.render_message_log(console, 32, 51, 35, 8,
                                self.engine.message_log)

        # Display the info pane
        self.render_info_pane(console, 69, 51)

    # Utility rendering functions

    def render_tiles(self, console):
        """Render the tile map."""

        # Get the current appearance for each tile
        current = self.engine.world.area.get_tile_appearances()

        # Draw the tiles
        console.tiles_rgb[0:self.engine.world.area.width,
                          0:self.engine.world.area.height] = current

    def render_contents(self, console):
        """Render the contents of a specific area."""

        # Loop through all the items
        for item in self.engine.world.area.items:
            # If the item is visible,
            if self.engine.world.area.is_visible(item.x, item.y):
                # Show the item
                console.print(item.x, item.y, item.char, item.colour)

        # Loop through all the entities
        for entity in self.engine.world.area.entities:

            # If the entity is visible,
            if self.engine.world.area.is_visible(entity.x, entity.y):
                # Show the entity
                console.print(entity.x, entity.y, entity.char, entity.colour)

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

    def render_status_pane(self, console, x, y, width):
        """Displays a status panel with key information about
           the area & player."""

        # Show key details
        console.print(x, y, self.engine.world.area.name, tcod.white)

        # Show the health bar
        self.render_bar(console, x, y + 2, width,
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

    def render_message_log(self, console, x, y, width, height, log):
        """Render the latest messages from the message log."""

        # Get the message lines
        messages = log.get_recent_wrapped_message_lines(width=width,
                                                        max_lines=height)

        offset = height - 1

        # Loop through the messages,
        for message in messages:

            # Display the message
            console.print(x, y + offset, message[0], message[1])

            # Up the offset
            offset -= 1
