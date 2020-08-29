"""
This module contains the implementation of the EventHandler class.
"""

import tcod.event


class PlayerEventHandler(tcod.event.EventDispatch):
    """Takes keyboard input and returns relevant commands."""

    def ev_quit(self, event):
        """Just end the program."""
        raise SystemExit()

    def ev_keydown(self, event):
        """If it's a keydown, handle it."""
        key = event.sym
        return key
