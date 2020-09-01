"""This file contains the implementation of the point class.
The class stores a position with x and y co-ordinates, so that
a position can be remembered even when its significance has
been lost."""


class Point:
    """Stores a single location."""
    def __init__(self, x, y):
        self.x = x
        self.y = y