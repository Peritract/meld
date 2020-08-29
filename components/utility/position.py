"""This module implements the Position class"""

from dataclasses import dataclass
from math import sqrt


@dataclass
class Position:
    """Stores a reference to an in-game location"""
    x: int = 0
    y: int = 0

    def distance_to(self, other):
        """Returns the distance between one point and another"""
        x_dist = other.x - self.x
        y_dist = other.y - self.y
        return sqrt(x_dist ** 2 + y_dist ** 2)
