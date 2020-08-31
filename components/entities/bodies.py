"""
This file contains the implementation of the "body"
class and its children.
"""


class Body:

    def __init__(self,
                 health=5,
                 attack=10,
                 defence=10):
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defence = defence
