"""
This file contains the implementation of the event class.
Various in-game events generate these objects.
"""

import tcod


class Event:

    def __init__(self, event_type="basic"):
        self.event_type = event_type


class Message(Event):

    def __init__(self, text, colour=tcod.white,
                 message_type="basic"):
        super().__init__(event_type="message")
        self.text = text
        self.colour = colour
        self.message_type = message_type


class Death(Event):

    def __init__(self, target):
        super().__init__(event_type="death")
        self.target = target
