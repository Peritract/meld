"""This file contains the necessary classes for creating
and displaying menus."""


class MenuOption:
    """A single menu option."""

    def __init__(self, name="Option", method=None):
        self.name = name
        self.method = method
