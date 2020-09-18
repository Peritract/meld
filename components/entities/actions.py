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


class Handle(Action):
    """Base class for any action with an item."""

    def __init__(self, item=None):
        self.item = item


class Move(Surge):
    """Movement to an adjacent tile."""

    def __init__(self, dx, dy):
        super().__init__(dx, dy)


class Attack(Action):
    """Melee attack."""

    def __init__(self, other):
        super().__init__()
        self.other = other


class PickUp(Handle):
    """Add an item to the inventory."""

    def __init__(self, item=None):
        super().__init__(item)


class Drop(Handle):
    """Transfer an item from the inventory to the area."""

    def __init__(self, item=None):
        super().__init__(item)


class Use(Handle):
    """Use an item."""

    def __init__(self, item=None):
        super().__init__(item)


class Equip(Handle):
    """Wield or wear an item."""

    def __init__(self, item=None):
        super().__init__(item)


class Unequip(Handle):
    """Return an item back to the inventory."""

    def __init__(self, item=None):
        super().__init__(item)


class Wait(Action):
    """Do nothing."""


class OpenMenu(Action):
    """Open the menu."""


class OpenInventory(Action):
    """Open the inventory."""
