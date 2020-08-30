"""
   This file conains the implementation of the world class.
   This class holds information about all the different levels
   of the game world, and information that needs to exist outside
   levels.
"""

# Temporary imports until proper generation
from ..entities.minds import Player
from .level import Level
from ..entities.entity import Entity
from ..utility.position import Position


class World:

    def __init__(self):

        # Hacky setup, one day to be extracted out to generators
        self.level = Level(40, 40)

        self.player = Entity("Miriam", Position(5, 5), Player)
        self.level.entities.append(self.player)

    def render(self, console):
        """Renders the current state of the game world."""

        # Pass the call down to the level
        self.level.render(console)

    def handle_actions(self):
        """Allows each entity to take a turn."""

        # Pass the call down to the level
        self.level.handle_actions()
