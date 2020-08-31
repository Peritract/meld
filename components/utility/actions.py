"""
This file holds the implementation of the action class
and its subclasses. Actions are used to store information
about entity movement/attacks/other.
"""


class Action:
    """Base action class."""

    # By default, does not end a turn
    final = False


class Surge(Action):

    # Ends turns
    final = True

    """Stores information about the direction of the action."""
    def __init__(self, dx, dy):
        super().__init__()
        self.dx = dx
        self.dy = dy


class Move(Surge):
    def __init__(self, dx, dy):
        super().__init__(dx, dy)


class Attack(Surge):
    def __init__(self, dx, dy, other):
        super().__init__(dx, dy)
        self.other = other


class Wait(Action):

    # Ends turns
    final = True
