"""
This module contains the implementation of the Engine class;
this class manages the game state and the window.
"""

import tcod
from ..world import World


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
                       "playing": self.play_game}

        # Holder for the current state
        self.state = "new_game"

    def start_main_loop(self):
        """Creates the main window and begins the game loop."""
        with tcod.context.new_terminal(self.width,
                                       self.height,
                                       tileset=self.tileset,
                                       title=self.title) as self.window:

            # Until the game is closed,
            while True:

                # Call the current state
                self.states[self.state]()

    def new_game(self):
        """
        Creates a new game world and populates it before
        changing the state to "play".
        """
        self.world = World()
        self.state = "playing"

    def play_game(self):
        """
        Function for the gameplay;
        lets entities move and updates the display.
        """

        # Display the game world as it currently is
        self.world.render(self.console)

        # Flush the console to the window
        self.window.present(self.console)

        # Clear the console, setting it up for the next turn
        self.console.clear()

        # Give entities the chance to act
        self.world.handle_turns()
