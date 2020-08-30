"""
This file contains the implementations of the various
AI "minds" - the logic for how each entity acts & takes turns.
"""

from ..utility.event_handlers import PlayerEventHandler
from ..utility.actions import Action
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

        # Start a loop until a turn-ending action
        complete = False
        while not complete:

            # Take user input
            for event in tcod.event.wait():

                # Check the event against valid actions
                decision = self.event_handler.dispatch(event)

                # Ignore invalid actions
                if not decision:
                    continue

                # Check if the action ends the turn
                complete = decision.final

        # Now a valid, turn-ending input has been found, return it.
        return decision
