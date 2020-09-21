"""This file contains the implementation of the ThrowState class.
This state allows the user to select an item and throw it."""

from .target_state import TargetState
from ...entities.actions import Throw


class ThrowState(TargetState):

    def __init__(self, engine, parent, item):
        super().__init__(engine, parent)
        self.item = item

    @property
    def target(self):
        """On confirmation, return to the game."""
        return Throw(self.item, self.cursor)
