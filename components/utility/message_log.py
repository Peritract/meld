"""
This file contains the implementation of the message log class and related
classes.
"""

from textwrap import wrap
import tcod


class Message:

    def __init__(self, text, colour=tcod.white,
                 message_type="basic"):
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


class MessageLog:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.messages = []

    def add_message(self, message):

        # If it's a duplicate
        if self.messages and self.messages[-1].text == message.text:
            # Increase the previous message's count
            self.messages[-1].count += 1

        else:
            # Add the message to the stack
            self.messages.append(message)

    def render_messages(self, console):
        """Draw messages on the console."""

        offset = self.height - 1
        for message in reversed(self.messages):
            # Display each message
            for line in reversed(wrap(message.get_full_text(), self.width)):
                console.print(self.x, self.y + offset,
                              message.get_full_text(),
                              message.colour)
                offset -= 1

                # If there's no more space
                if offset < 0:
                    # Stop writing lines
                    return
