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
    """Base class for any action with a direction."""

    # Ends turns
    final = True

    def __init__(self, dx, dy):
        super().__init__()
        self.dx = dx
        self.dy = dy


class Move(Surge):
    """Movement to an adjacent tile."""

    def __init__(self, dx, dy):
        super().__init__(dx, dy)


class Attack(Action):
    """Melee attack."""

    def __init__(self, other):
        super().__init__()
        self.other = other


class Wait(Action):
    """Do nothing."""

    # Ends turns
    final = True
