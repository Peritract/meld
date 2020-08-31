"""
This file contains the implementations of the various
AI "minds" - the logic for how each entity acts & takes turns.
"""

from ..utility.event_handlers import PlayerEventHandler
from ..utility.actions import Surge, Move, Attack
import tcod.event


class Mind():
    """The base mind class."""

    def take_action(self, level):
        # Generic turn-taking function
        print('The ' + self.owner.name + ' moves in mysterious ways.')


class Player(Mind):
    """The mind class for a player-controlled character."""

    def __init__(self):
        self.event_handler = PlayerEventHandler()

    def take_action(self, level):

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

                # If the action has a direction,
                if isinstance(decision, Surge):

                    # Check that the direction is valid
                    new_x = self.owner.x + decision.dx
                    new_y = self.owner.y + decision.dy
                    if not level.in_bounds(new_x, new_y) or \
                       not level.is_passable(new_x, new_y):
                        continue

                    # If there is an entity in the way
                    entity = level.get_blocking_entity(new_x, new_y)
                    if entity:
                        decision = Attack(decision.dx, decision.dy, entity)

                    # Otherwise
                    else:
                        decision = Move(decision.dx, decision.dy)

                # Check if the action ends the turn
                complete = decision.final

                # If the action completes, jump out of the for loop
                if complete:
                    break

        # Now a valid, turn-ending input has been found, return it.
        return decision
