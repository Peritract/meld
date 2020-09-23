"""
This file contains the implementation of the base Area class.
This is a single in-game location.
"""

from ..entities.entity import Entity
from ..environments.tiles import basic_floor, unknown
from ..items.items import Item
import numpy as np
from tcod.map import compute_fov
from ..utilities.constants import DIRECTIONS
import tcod


class Area:
    """An in-game location."""

    def __init__(self, width, height, world, name="area"):
        self.width = width
        self.height = height
        self.world = world
        self.name = name

        # Holders for all internal objects
        self.contents = set()

        # ---HACK--- #

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

        # ---/HACK--- #

    @property
    def entities(self):
        """Returns a set of entities in the area."""
        return set([thing for thing in self.contents
                    if isinstance(thing, Entity)])

    @property
    def items(self):
        """Returns as set of items in the area."""
        return set([thing for thing in self.contents
                    if isinstance(thing, Item)])

    def is_free(self, x, y):
        """Checks if a given tile is inbounds, passable, and unoccupied."""
        return self.is_passable(x, y) and not self.get_blocker_at_location(x,
                                                                           y)

    def is_visible(self, x, y):
        """Checks if a given point is visible."""
        if self.in_bounds(x, y):
            return self.visible_tiles[x, y]
        return False

    def is_passable(self, x, y):
        """Checks if a given tile is passable."""
        if self.in_bounds(x, y):
            return self.tiles[x, y]["passable"]
        return False

    def in_bounds(self, x, y):
        """Checks if a given point is inside the area bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def at_location(self, x, y):
        """Returns a set of objects at the given location."""
        if self.in_bounds(x, y):
            return set([thing for thing in self.contents
                        if thing.x == x and thing.y == y])

    def distance_between(self, a, b):
        """Gets the absolute difference between two tile locations."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_directly_adjacent_tiles(self, x, y, passable=True):
        """Gets the adjacent tiles to a tile."""

        # Get a list of direct neighbours
        neighbours = [(x + dir[0], y + dir[1]) for dir in DIRECTIONS.values()]

        # If passable=True, filter the list for passable locations
        if passable:
            neighbours = filter(lambda x: self.is_passable(*x), neighbours)

        # otherwise, just check that the neighbours are in bounds
        else:
            neighbours = filter(lambda x: self.in_bounds(*x), neighbours)

        # return the list of locations
        return list(neighbours)

    def get_tiles_in_range(self, x, y, range):
        """Returns the location of passable tiles that can be reached from a starting
           tile within a particular radius."""

        # Holder for valid tiles
        tiles = [(x, y)]

        # Tiles to explore
        edge = self.get_directly_adjacent_tiles(x, y)

        # BFS for tiles in range
        while edge:
            curr = edge.pop()
            tiles.append(curr)
            potentials = self.get_directly_adjacent_tiles(curr[0],
                                                          curr[1])
            for tile in potentials:
                if tile not in edge and tile not in tiles:
                    if self.distance_between((x, y), tile) < range:
                        edge.append(tile)

        return tiles

    def items_at_location(self, x, y):
        """Returns the set of pick-upable items at the location."""
        contents = self.at_location(x, y)
        if contents:
            return {x for x in contents if isinstance(x, Item)}

    def add_contents(self, addition):
        """Adds new objects to the level."""
        if not isinstance(addition, list):
            self.contents.add(addition)
            addition.area = self
        else:
            self.contents = self.contents.union(set(addition))
            for thing in addition:
                thing.area = self

    def remove_contents(self, contents):
        """Removes objects from the level."""
        if not isinstance(contents, list):
            self.contents.remove(contents)
            contents.area = None
        else:
            self.contents = self.contents.difference(set(contents))
            for thing in contents:
                thing.area = None

    def get_blocker_at_location(self, x, y):
        """Returns the blocking entity at a particular position."""

        # Get all objects on the tile
        present = self.at_location(x, y)

        for thing in present:
            if thing.blocks:
                return thing

    def calculate_fov(self, entity):
        """Returns the visible area for a particular entity"""

        # Get a map the size of the level
        visible = np.full((self.width, self.height),
                          fill_value=False,
                          order="F")

        # Compute field of view from the entity's location
        visible[:] = compute_fov(self.tiles["transparent"],
                                 (entity.x, entity.y),
                                 radius=entity.body.view_radius,
                                 algorithm=tcod.FOV_SHADOW)

        # Return the visible map
        return visible

    def get_tile_appearances(self):
        """Get the current appearance of each tile."""
        return np.select(condlist=[self.visible_tiles,
                                   self.explored_tiles],
                         choicelist=[self.tiles["in_view"],
                                     self.tiles["out_of_view"]],
                         default=unknown)

    def update_tile_states(self, entity):
        """Updates the state of tiles (visible/explored)
           based on a given entity."""

        # Update the visible tiles based on the player's FoV
        self.visible_tiles = self.calculate_fov(entity)

        # Update explored tiles based on the visible ones
        # Set explored to equal explored | visible (preserve any Trues in
        # either)
        self.explored_tiles |= self.visible_tiles

    def get_path_to(self, actor, x, y):
        """Finds a route to between an entity and a position."""

        # Get the cost map
        cost = actor.get_tile_costs()

        # Convert the map to a graph (disallow diagonal movement)
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=0)

        # Make a pathfinder
        finder = tcod.path.Pathfinder(graph)
        finder.add_root((actor.x, actor.y))

        # Find a path if possible
        path = finder.path_to((x, y)).tolist()

        # If movement is possible
        if path:
            # Return all the path except the starting point
            return path[1:]
        else:
            # No path can be found
            return None

    def get_direct_path_to(self, start, end):
        """Return the direct path from the start to the end."""
        """Line of sight."""
        return tcod.los.bresenham(start, end)

    # Utility functions

    def post_message(self, message):
        """Adds a message to the associated message log."""
        self.world.engine.message_log.add_message(message)
