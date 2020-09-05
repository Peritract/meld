"""
This file contains the implementation of the message log class.
"""

from textwrap import wrap
from .events import Message


class MessageLog:

    def __init__(self):
        self.messages = [Message("Working title Roguelike.")]

    def add_message(self, message):
        # If it's a duplicate
        if self.messages[-1].text == message.text:
            # Increase the previous message's count
            self.messages[-1].count += 1

        else:
            # Add the message to the stack
            self.messages.append(message)

    def render_messages(self, console, x, y, width, height):
        """Draw messages on the console."""

        offset = height - 1
        for message in reversed(self.messages):
            # Display each message
            for line in reversed(wrap(message.get_full_text(), width)):
                console.print(x, y + offset,
                              message.get_full_text(),
                              message.colour)
                offset -= 1

                # If there's no more space
                if offset < 0:
                    # Stop writing lines
                    return
