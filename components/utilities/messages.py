"""
This file contains the implementation of the Message class and related
classes.
"""

from textwrap import wrap
from .constants import COLOURS as C


class Message:
    """A single in-game message."""

    def __init__(self, text, colour=C["WHITE"]):
        self.text = text
        self.colour = colour
        self.count = 1

    def get_full_text(self):

        # If it's a duplicate
        if self.count > 1:
            # Add on the count
            return f"{self.text} (x{self.count})"
        return self.text

# Different message types


class CombatMessage(Message):
    """A violent act."""
    def __init__(self, text):
        super().__init__(text, C["RED"])


class SystemMessage(Message):
    """An error or exception."""
    def __init__(self, text):
        super().__init__(text, C["YELLOW"])


class WorldMessage(Message):
    """A global event."""
    def __init__(self, text):
        super().__init__(text, C["PURPLE"])


class ItemMessage(Message):
    """An item changes hands or state."""
    def __init__(self, text):
        super().__init__(text, C["BROWN"])


class AlertMessage(Message):
    """A sudden and shocking change."""
    def __init__(self, text):
        super().__init__(text, C["GREEN"])


class DeathMessage(Message):
    """The brutal end of a short life."""
    def __init__(self, text):
        super().__init__(text, C["GREY"])


class MessageLog:
    """Holder and manager for in-game messages."""

    def __init__(self):
        self.messages = []

    @property
    def length(self):
        return len(self.messages)

    def add(self, message):
        """Log a message."""

        # If it's a duplicate
        if self.messages and self.messages[-1].text == message.text:
            # Increase the previous message's count
            self.messages[-1].count += 1

        else:
            # Add the message to the stack
            self.messages.append(message)

    def get_message_lines(self, reverse=True, width=20,
                          max_lines=10):
        """Returns a list of message lines, wrapped to the log width."""

        lines = []

        # Set message order
        messages = reversed(self.messages) if reverse else self.messages

        # Loop through the messages
        for message in messages:
            # Calculate the line breaks
            for line in reversed(wrap(message.get_full_text(), width)):

                # Add each line to the log, with colour information
                lines.append((line, message.colour))

                # If the line-length has been hit
                if max_lines != -1 and max_lines <= len(lines):

                    # Return the set
                    return lines

        return lines
