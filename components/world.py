"""
   This file conains the implementation of the world class.
   This class holds information about all the tiles and objects
   in the game world.
"""

from .entities.entity import Entity
from .utility.position import Position


class World:

    def __init__(self):
        self.entities = {Entity("Chett"), Entity("Victoria", Position(1, 3))}

    def render(self, console):
        """Renders the current state of the game world."""

        for entity in self.entities:
            console.print(entity.position.x,
                          entity.position.y,
                          entity.character,
                          entity.colour)

    def handle_turns(self):
        """Allows each non-player entity to take a turn."""
        for entity in self.entities:
            entity.mind.take_turn()
