"""This file contains the implementation of the LookState class.
This state allows the user to look around with the keys/mouse."""

from .target_state import TargetState


class LookState(TargetState):

    def __init__(self, engine, parent):
        super().__init__(engine, parent)

    def target(self):
        """On confirmation, return to the game."""
        return None
