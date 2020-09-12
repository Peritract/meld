"""
This file contains the implementation of the GameOverState class.
This class wraps everything up and presents the player with
the only valid options.
"""

from .state import State


class GameOverState(State):

    def __init__(self, engine):
        super().__init__(engine)

    def render(self, console):
        print("GAME OVER, MAN, GAME OVER!")
