"""
This file contains the implementations of the various
AI "minds" - the logic for how each entity acts & takes turns.
"""

from ..utility.event_handlers import PlayerEventHandler
import tcod.event


class Mind():
    """The base mind class."""

    def take_turn(self):
        # Generic turn-taking function
        print('The ' + self.owner.name + ' wonders when it will get to move.')


class Player(Mind):
    """The mind class for a player-controlled character."""

    def __init__(self):
        self.event_handler = PlayerEventHandler()

    def take_turn(self):
        print("TAKIN' A TURN!")
        # Take user input
        result = None
        while not result:
            for event in tcod.event.wait():
                result = self.event_handler.dispatch(event)
