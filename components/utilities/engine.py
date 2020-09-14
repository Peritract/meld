"""
This file implements the engine class;
An instance of this class manages the
game screen and states.
"""

import tcod
from .states.play_state import PlayState
from .states.game_over_state import GameOverState
from .states.main_menu_state import MainMenuState
from .states.new_game_state import NewGameState


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
        self.states = {"main_menu": MainMenuState(self),
                       "new_game": NewGameState(self),
                       "play_game": PlayState(self),
                       "game_over": GameOverState(self)}
        self.state = "main_menu"

        # Mouse location
        self.m_loc = (0, 0)

        # Message storage
        self.message_log = None

    def set_state(self, state):
        """Changes the engine state."""
        self.state = state

    def run_main_loop(self):
        """Repeatedly calls the current state method."""

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
