"""This file contains the implementation of the event log
   and its related classes.
"""

from datetime import datetime


class Event:

    def __init__(self, level=None):
        self.level = level
        self.time = datetime.now()


class Death(Event):

    def __init__(self, target):
        super().__init__("level")
        self.target = target


class GameOver(Event):

    def __init__(self):
        super().__init__("engine")


class EventLog:

    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def remove_event(self, event):
        self.events.remove(event)

    def get_filtered_events(self, level):
        return [x for x in self.events if x.level == level]
