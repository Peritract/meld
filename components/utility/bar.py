"""
This file contains the necessary functions to display progress bars.
"""


def render_bar(console, x, y, value,
               max_value, max_width, colour,
               background, caption, caption_colour):
    """Displays a bar with a varied width."""

    # Calculate the width
    width = int(value / max_value * max_width)

    # Display the background
    console.draw_rect(x, y, max_width, 1, 1, bg=background)

    # If there's anything on the bar
    if width > 0:
        # Draw the bar over the top
        console.draw_rect(x, y, width, 1, 1, bg=colour)

    # Put the numbers over the top
    console.print(x, y, f"{caption}: {value}/{max_value}", caption_colour)
