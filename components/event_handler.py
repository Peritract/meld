"""
This module contains the implementation of the EventHandler class.
"""

import tcod.event


class EventHandler(tcod.event.EventDispatch):
    """Takes keyboard input and returns relevant commands."""

    def ev_quit(self, event):
        raise SystemExit()

    def ev_keydown(self, event):
        key = event.sym
        print(key)
