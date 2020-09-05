"""
This file contains the implementation of the status panel;
it displays key information about the player.
"""

from .bar import render_bar
import tcod


class StatusPanel:

    def __init__(self, x, y, width, height):

        # Where the panel will be displayed
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self, player, level, console):
        """Renders player & level information."""

        # Show key details
        console.print(self.x, self.y, f"Level {level.index}", tcod.white)

        # Show the health bar
        render_bar(console, self.x, self.y + 1, player.body.health,
                   player.body.max_health, 30, tcod.dark_green,
                   tcod.dark_gray, "Health", tcod.white)
