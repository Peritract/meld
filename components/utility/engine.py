"""
This module contains the implementation of the Engine class;
this class manages the game state and the window.
"""

import tcod
from ..environment.world import World
from .message_log import MessageLog
from .status_panel import StatusPanel
from .event_log import EventLog, GameOver


class Engine:
    """Runs the game loop and manages the screen and game states"""

    def __init__(self, width, height, tileset, title="Working Title"):
        """Sets internal engine variables."""
        self.width = width
        self.height = height
        self.title = title

        # Load the font file
        self.tileset = tcod.tileset.load_tilesheet("./assets/arial12x12.png",
                                                   32, 8,
                                                   tcod.tileset.CHARMAP_TCOD)

        # Create the console for drawing on
        self.console = tcod.Console(self.width, self.height, order="F")
        # Order=F flips x and y, for easier drawing

        # Holder for states
        self.states = {"new_game": self.new_game,
                       "playing": self.play_game,
                       "game_over": self.game_over}

        # Holder for the current state
        self.state = "new_game"

    def start_main_loop(self):
        """Creates the main window and begins the game loop."""
        with tcod.context.new_terminal(self.width,
                                       self.height,
                                       tileset=self.tileset,
                                       title=self.title) as self.window:

            # Flag for the game running
            while True:

                # Call the current state
                self.states[self.state]()

    def new_game(self):
        """
        Creates a new game world and populates it before
        changing the state to "play".
        """

        # Create a game world
        self.world = World(self, 80, 50)

        # Create the event log
        self.event_log = EventLog()

        # The message log
        self.message_log = MessageLog(38, 50, 40, 10)

        # The status panel
        self.status_panel = StatusPanel(0, 50, 30, 10)

        # Change state from new to playing
        self.state = "playing"

    def play_game(self):
        """
        Function for the gameplay;
        lets entities move and updates the display.
        """

        # Clear the console, removing old things
        self.console.clear()

        # Display the current state of the game world
        self.world.render(self.console)
        self.message_log.render_messages(self.console)
        self.status_panel.render(self.console, self.world)

        # Flush the console to the window
        self.window.present(self.console)

        # Give entities the chance to act
        self.world.handle_actions()

        # Handle engine-level events
        for event in self.event_log.get_filtered_events("engine"):
            if isinstance(event, GameOver):
                self.state = "game_over"

            # Remove the event from the log
            self.event_log.remove_event(event)

    def game_over(self):
        """Ends the game."""

        print("It's all over.")

        raise SystemExit()
