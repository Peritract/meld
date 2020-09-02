"""
This file contains the implementation of the "body"
class and its children.
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
