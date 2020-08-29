"""
    This file contains the implementation of the base Entity class;
    An entity is any object more complex than a simple physical item.
"""

from ..utility.object import Object
from ..utility.position import Position


class Entity(Object):
    """The base class for all animate game objects"""

    def __init__(self, name="entity", position=Position(0, 0)):
        """Sets internal properties"""
        Object.__init__(self, position)
        self.name = name
