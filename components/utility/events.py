"""
This file contains the implementation of the event class.
Various in-game events generate these objects.
"""

import tcod
from datetime import datetime


class Event:

    def __init__(self):
        self.time = datetime.now()


class Message(Event):

    def __init__(self, text, colour=tcod.white,
                 message_type="basic"):
        super().__init__()
        self.text = text
        self.colour = colour
        self.message_type = message_type
        self.count = 1

    def get_full_text(self):

        # If it's a duplicate
        if self.count > 1:
            # Add on the count
            return f"{self.text} (x{self.count})"
        return self.text


class Death(Event):

    def __init__(self, target):
        super().__init__()
        self.target = target


class GameOver(Event):

    def __init__(self):
        super().__init__()
