"""
This module contains the implementation of the EventHandler class.
"""

import tcod.event
from .actions import Surge, Wait, Inspect, MouseOver


class PlayerEventHandler(tcod.event.EventDispatch):
    """Takes keyboard input and returns relevant commands."""

    def ev_quit(self, event):
        """Just end the program."""
        raise SystemExit()

    def ev_keydown(self, event):
        """If it's a keydown, handle it."""
        key = event.sym
        action = None

        # Movement keys
        if key == tcod.event.K_UP:
            action = Surge(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = Surge(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = Surge(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = Surge(dx=1, dy=0)
        elif key == tcod.event.K_PERIOD:
            action = Wait()

        # Interface keys
        elif key == tcod.event.K_l:
            action = Inspect()

        return action


class InspectEventHandler(tcod.event.EventDispatch):
    """Takes mouse & keyboard input."""

    def ev_quit(self, event):
        """Just end the program."""
        raise SystemExit()

    def ev_keydown(self, event):
        """Look out for events leaving the mode."""
        key = event.sym

        if key == tcod.event.K_l or key == tcod.event.K_ESCAPE:
            return Inspect()

    def ev_mousemotion(self, event):
        return MouseOver(event.tile.x, event.tile.y)
