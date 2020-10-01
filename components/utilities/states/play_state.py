"""
This file contains the implementation of the PlayState class.
This is the "game" bit - it manages turn-taking and level/unit display.
"""

from ...entities.actions import (Surge, Wait, PickUp, Interact,
                                 OpenMenu, OpenInventory, Look,
                                 Activate, ViewLog)
from ...entities.entity import Entity
from .state import State
from .in_game_menu import InGameMenu
from .text_states import MessageScroller
from ..constants import DIRECTIONS, COLOURS as C
from ..messages import SystemMessage
from ..exceptions import Impossible
import tcod


class Play(State):
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
            action = Surge(*DIRECTIONS["UP"])
        elif key == tcod.event.K_DOWN:
            action = Surge(*DIRECTIONS["DOWN"])
        elif key == tcod.event.K_LEFT:
            action = Surge(*DIRECTIONS["LEFT"])
        elif key == tcod.event.K_RIGHT:
            action = Surge(*DIRECTIONS["RIGHT"])

        # Pass the turn
        elif key == tcod.event.K_PERIOD:
            action = Wait()

        # Collect an object
        elif key == tcod.event.K_g:
            action = PickUp()

        # Open the inventory
        elif key == tcod.event.K_i:
            action = OpenInventory()

        # Open a menu
        elif key == tcod.event.K_ESCAPE:
            action = OpenMenu()

        # View the message log
        elif key == tcod.event.K_m or key == tcod.event.K_v:
            action = ViewLog()

        # Look around
        elif key == tcod.event.K_l or key == tcod.event.K_k:
            action = Look()

        # Interact with objects
        elif key == tcod.event.K_RETURN or key == tcod.event.K_u:
            action = Interact()

        # Activate an ability
        elif key == tcod.event.K_a:
            action = Activate()

        return action

    def handle_event(self, action):
        """Advances the turn if a valid action has been taken."""

        # If no action has been chosen, pass on
        if not action:
            return

        # If the action is to open a menu
        if isinstance(action, OpenMenu):

            # Set the temporary state
            self.engine.set_state(InGameMenu(self.engine, self))

            # Return so the new state can work
            return

        elif isinstance(action, ViewLog):

            # Set the temporary state
            self.engine.set_state(MessageScroller(self.engine, self))

            # Return so the new state can work
            return

        # Pass the action to the player
        try:
            self.engine.world.player.take_action(action)

        # Unless the action is meaningless,
        except Impossible as ex:
            self.engine.message_log.add(SystemMessage(ex.args[0]))
            return

        # If the state hasn't changed,
        if self.engine.state == self:

            # Update the player state
            self.engine.world.player.update()

            # Let all other entities take turns
            for entity in self.engine.world.entities - \
                    {self.engine.world.player}:
                entity.take_action()
                entity.update()

            # Update all the features
            for feature in self.engine.world.features:
                feature.act()

    def render(self, console):
        """Display the current state of the game world."""

        # Update tile appearances
        self.engine.world.area.update_tile_states(self.engine.world.player)

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
        self.render_info_pane(console, 69, 51, 8)

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

        contents = sorted(self.engine.world.area.contents,
                          key=lambda x: x.render_order.value)

        for thing in contents:
            if self.engine.world.area.is_visible(thing.x, thing.y):
                # Show the entity
                console.print(thing.x, thing.y, thing.char,
                              thing.colour)

    def render_info_pane(self, console, x, y, height):
        """Displays information about the tile under the mouse."""

        # If the mouse is over a visible tile
        if self.engine.world.area.is_visible(*self.engine.m_loc):

            # Get the tile contents
            contents = self.engine.world.area.at_location(*self.engine.m_loc)

            # If there is anything to display
            if contents:
                rows = 0
                # Display it (entities first)
                for thing in sorted(contents,
                                    key=lambda x: not isinstance(x, Entity)):
                    console.print(x, y, thing.name, thing.colour)
                    y += 2
                    rows += 2

                    # Only display rows up until the height
                    if rows >= height:
                        return

    def render_status_pane(self, console, x, y, width):
        """Displays a status panel with key information about
           the area & player."""

        # Show key details
        console.print(x, y, self.engine.world.area.name, C["WHITE"])

        # Show the health bar
        self.render_bar(console, x, y + 2, width,
                        self.engine.world.player.body.health,
                        self.engine.world.player.body.max_health,
                        C["GREY"], C["GREEN"], "Health",
                        C["WHITE"])

    def render_bar(self, console, x, y, max_width,
                   value=0, max_value=10,
                   background_colour=tcod.dark_gray,
                   colour=tcod.dark_blue,
                   caption="", caption_colour=C["WHITE"]):
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
        messages = log.get_message_lines(width=width,
                                         max_lines=height)

        offset = height - 1

        # Loop through the messages,
        for message in messages:

            # Display the message
            console.print(x, y + offset, message[0], message[1])

            # Up the offset
            offset -= 1
