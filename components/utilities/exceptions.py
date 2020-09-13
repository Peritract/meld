"""This file contains the custom exceptions necessary for the game."""


class Impossible(Exception):
    """Attempted the impossible"""


class InventoryFull(Exception):
    """Tried to pick up something while carrying too much."""