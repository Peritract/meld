"""
This file implements the engine class;
An instance of this class manages the
game screen and states.
"""

import tcod
from .play_state import PlayState
from .message_log import MessageLog, Message


class Engine:
    """Manages the game screen and states."""

    def __init__(self, screen_title, screen_width, screen_height, font):
        """Sets key variables."""

        # Screen appearance
        self.screen_title = screen_title
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.tileset = tcod.tileset.load_tilesheet("./assets/arial12x12.png",
                                                   32, 8,
                                                   tcod.tileset.CHARMAP_TCOD)

        # Drawing console
        # Order=F flips x and y, for easier drawing
        self.console = tcod.Console(self.screen_width, self.screen_height,
                                    order="F")

        # State management
        self.states = {"play_game": PlayState(self)}
        self.state = "play_game"

        # Mouse location
        self.m_loc = (0, 0)

        # Message storage
        self.message_log = MessageLog()

    def run_main_loop(self):
        """Repeatedly calls the current state method."""

        # TEMPORARY, I HOPE I HOPE I HOPE
        self.hack()

        # Make the window
        """Creates the main window and begins the game loop."""
        with tcod.context.new_terminal(self.screen_width,
                                       self.screen_height,
                                       tileset=self.tileset,
                                       title=self.screen_title) as window:

            # Flag for the game running
            while True:

                # Clear the window
                self.console.clear()

                # Render the current state
                self.states[self.state].render(self.console)

                # Flush the console to the window
                window.present(self.console)

                # Call the current state's event handler
                self.states[self.state].handle_events(window)

    def hack(self):
        """Short-term values for development that will one day be removed."""
        from ..entities.entity import Entity
        from ..entities.player_entity import Player
        from ..environments.world import World
        from ..environments.area import Area
        from ..environments.tiles import basic_wall

        self.world = World(self)
        self.player = Player("player", 5, 5)
        other = Entity("other", 10, 10)
        area = Area(80, 50, self.world)
        area.tiles[30:33, 22] = basic_wall
        self.message_log.add_message(Message("I am alive!"))
        self.world.areas.append(area)
        self.world.current_area = 0
        self.world.area.contents = self.world.area.contents.union({self.player,
                                                                   other})
