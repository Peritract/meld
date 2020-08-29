"""
This file contains the implementations of the various
AI "minds" - the logic for how each entity acts & takes turns.
"""


class Mind():
    """The base mind class."""

    def take_turn(self):
        # Generic turn-taking function
        print('The ' + self.owner.name + ' wonders when it will get to move.')