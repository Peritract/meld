"""
This file contains the implementation of the Body class.
This class stores physical information about in-game entities.
"""


class Body:

    def __init__(self,
                 health=5,
                 attack=12,
                 defence=10,
                 view_radius=5):
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defence = defence
        self.view_radius = view_radius
        self.carry_capacity = 3
