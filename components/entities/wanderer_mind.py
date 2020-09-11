"""This file contains the implementation of the wanderer AI.
This mind chooses passive, random movement.
"""

from .mind import Mind
from .actions import Move, Wait
from random import choice
from ..utilities.constants import directions


class Wanderer(Mind):
    """Moves randomly, with no awareness."""

    def make_decision(self, area):

        # Makes a choice - move or not
        move = choice([True, False])

        # If movement is chosen,
        if move:

            # Check the four possible options (valid, passable & unoccupied)
            options = filter(lambda x: area.is_movable(self.owner.x + x[0],
                                                       self.owner.y + x[1]),
                             directions.values())

            # Convert to list
            options = list(options)

            # Pick an option at random
            if options:
                direction = choice(options)

                if direction:
                    return Move(*direction)

        # If nothing else is possible, wait
        return Wait()
