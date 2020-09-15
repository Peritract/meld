"""
This file holds the implementation of the action class
and its subclasses. Actions are used to store information
about entity movement/attacks/other.
"""


class Action:
    """Base action class."""


class Surge(Action):
    """Base class for any action with a direction."""

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


class PickUp(Action):
    """Add an item to the inventory."""

    def __init__(self, item=None):
        self.item = item


class Drop(Action):
    """Remove an item from the inventory."""

    def __init__(self, item=None):
        self.item = item


class Wait(Action):
    """Do nothing."""


class OpenMenu(Action):
    """Open the menu."""


class OpenInventory(Action):
    """Open the inventory."""
