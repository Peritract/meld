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
