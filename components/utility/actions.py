"""
This file holds the implementation of the action class
and its subclasses. Actions are used to store information
about entity movement/attacks/other.
"""


class Action:
    """Base action class."""

    # By default, does not end a turn
    final = False


class Movement(Action):

    # Ends turns
    final = True

    """Stores information about entity movement."""
    def __init__(self, dx, dy):
        super().__init__()
        self.dx = dx
        self.dy = dy
