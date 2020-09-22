"""This file contains the implementation of the LoadGame state.
This state loads a game from a file, if possible.
"""

from .state import State
from .play_state import Play


class LoadGame(State):
    """Loads the game from a file."""

    def __init__(self, engine):
        super().__init__(engine)

    def render(self):
        """No display required."""
        pass

    def handle_events(self, window):
        """Doesn't actually handle events; attempts to load the game."""

        # Change the state to playing
        self.engine.set_state(Play(self.engine))
