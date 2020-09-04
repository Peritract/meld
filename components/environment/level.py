"""
This file contains the implementation of the LevelMap
class - this stores the map for a single in-game area.
"""

import numpy as np
from .tiles import unknown, basic_floor, basic_wall
from ..entities.entity import Entity
from tcod.map import compute_fov
from math import sqrt

import tcod
from ..entities.minds import Hunter
from ..utility.events import Message, Death, GameOver


class Level:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Create a map of floor tiles, with x and y humanised.
        self.tiles = np.full((width, height),
                             fill_value=basic_floor,
                             order="F")

        # holders for details of visible/known tiles
        self.visible_tiles = np.full((width, height),
                                     fill_value=False,
                                     order="F")
        self.explored_tiles = np.full((width, height),
                                      fill_value=False,
                                      order="F")

        # Holders for the creatures and items
        self.entities = []
        self.items = []

        # Trash wall, for the exampling
        self.tiles[30:33, 22] = basic_wall

        # Trash entities, for the exampling
        self.entities.append(Entity("Victoria", (1, 1), mind=Hunter))

    # Utility functions - mostly about checking tiles for particular purposes

    def in_bounds(self, x, y):
        """Checks if a given point is inside the map bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_passable(self, x, y):
        """Checks if a tile in a given location is passable."""
        if self.tiles["passable"][x, y]:
            return True
        return False

    def distance_to(self, a, b):
        """Returns the distance between one point and another"""
        x_dist = a.x - b.x
        y_dist = a.y - b.y
        return sqrt(x_dist ** 2 + y_dist ** 2)

    def get_adjacent_spaces(self, x, y):
        """Gets adjacent spaces - non-blocked, in-bounds tiles.
        Returns a list of relative coordinates
        """
        directions = {(0, 1), (0, -1), (1, 0), (-1, 0)}
        spaces = []
        for dir in directions:
            space = (x + dir[0], y + dir[1])
            if self.in_bounds(*space) and self.is_passable(*space):
                spaces.append(dir)
        return spaces

    # Rendering and FoV methods

    def get_fov(self, center):
        """Returns the visible area for a particular entity"""

        # Get a map the size of the level
        visible = np.full((self.width, self.height),
                          fill_value=False,
                          order="F")

        # Compute field of view from the center
        visible[:] = compute_fov(self.tiles["transparent"],
                                 (center.x, center.y),
                                 radius=center.body.view_radius,
                                 algorithm=tcod.FOV_SHADOW)

        # Return the visible map
        return visible

    def render(self, console, player):
        """Displays the game world on a given console."""

        # Update the visible tiles based on the player's FoV
        self.visible_tiles = self.get_fov(player)

        # Update explored tiles based on the visible ones
        # Set explored to equal explored | visible (preserve any Trues in
        # either)
        self.explored_tiles |= self.visible_tiles

        # Fill the map with tiles, choosing the correct appearance for each one
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible_tiles, self.explored_tiles],
            choicelist=[self.tiles["in_view"], self.tiles["out_of_view"]],
            default=unknown)

        # Display each item
        for item in self.items:

            # If it's in view
            if self.visible_tiles[item.x, item.y]:
                console.print(item.x,
                              item.y,
                              item.char,
                              item.colour)

        # Display each entity
        for entity in self.entities:

            # If it's in view
            if self.visible_tiles[entity.x, entity.y]:
                console.print(entity.x,
                              entity.y,
                              entity.char,
                              entity.colour)

    # Entity management

    def get_blocking_entity(self, x, y):
        """Returns the blocking entity at a particular position."""
        for entity in self.entities:
            if entity.blocks and entity.x == x and entity.y == y:
                return entity
        return None

    def handle_actions(self, player):
        """Allow each entity to act."""

        # Holder for events (game-changing ones)
        world_events = []

        # Loop through the entities
        for entity in self.entities:

            # Let each one take a turn
            events = entity.take_action(self)

            # Handle any events passed back
            for event in events:

                # Display messages
                if isinstance(event, Message):
                    world_events.append(event)

                # Handle dead entities
                elif isinstance(event, Death):

                    # Call the die method, passing in the level
                    message = event.target.die(self)

                    # Log the message
                    world_events.append(message)

                    # If the dead entity is the player,
                    world_events.append(GameOver())

        return world_events
