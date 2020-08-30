"""
   This file conains the implementation of the world class.
   This class holds information about all the tiles and objects
   in the game world.
"""

from .entities.entity import Entity
from .utility.position import Position

# Temporary import until proper generation
from .entities.minds import Player


class World:

    def __init__(self):
        self.player = Entity("Miriam", Position(5, 5), Player)
        self.entities = [Entity("Chett"),
                         Entity("Victoria", Position(1, 1)),
                         Entity("Victoria", Position(2, 2))]
        self.entities.append(self.player)

    def render(self, console):
        """Renders the current state of the game world."""

        for entity in self.entities:
            console.print(entity.position.x,
                          entity.position.y,
                          entity.character,
                          entity.colour)

    def handle_turns(self):
        """Allows each entity to take a turn."""
        for entity in self.entities:
            entity.take_turn()
