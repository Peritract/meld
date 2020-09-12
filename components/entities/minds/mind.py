"""
This file contains the implementation of the basic "mind" class
 - the logic for how each entity acts & takes turns.
"""

from ..actions import Wait


class Mind():
    """The base mind class."""

    def make_decision(self, area):
        """Make a decision about what to do."""

        return Wait()
