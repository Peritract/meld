"""This file contains the implementation of the ItemSelectionMenu.
This state displays a list of items fro the player to choose from."""

from .menus import OverlayMenu, MenuOption
from ...entities.actions import PickUp, Activate


class ItemSelectionMenu(OverlayMenu):
    """Presents the player with a list of items to choose from."""

    def __init__(self, engine, parent, items):
        super().__init__(engine, parent)
        self.items = items
        self.options = self.parse_items()

    def parse_items(self):
        """Converts a set of items into menu options."""
        return [MenuOption(x.name, value=PickUp(x)) for x in self.items]


class AbilitySelectionMenu(OverlayMenu):
    """Presents the player with a list of abilities to choose from."""

    def __init__(self, engine, parent, abilities):
        super().__init__(engine, parent)
        self.abilities = abilities
        self.options = self.parse_abilities()

    def parse_abilities(self):
        """Converts a set of abilities into menu options."""
        return [MenuOption(x.name, value=Activate(x)) for x in self.abilities]
