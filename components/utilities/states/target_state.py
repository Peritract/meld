"""This file contains the implementation of the TargetState class
and its subclasses; these classes allow the user to select a given
in-game tile.
"""

from .state import State
from ..constants import DIRECTIONS, COLOURS as C
from ...entities.actions import Throw
import tcod


class TargetState(State):
    """Allows the user to select a target tile/entity."""

    def __init__(self, engine, parent):
        super().__init__(engine)
        self.parent = parent

        # Start at the player's position
        self.set_cursor(self.engine.world.player.x,
                        self.engine.world.player.y)

    @property
    def cursor(self):
        return self.engine.m_loc

    def set_cursor(self, x, y):
        """Change the cursor position."""
        self.engine.m_loc = (x, y)

    def move_cursor(self, direction, mod):
        """Move the cursor in a particular direction."""
        x, y = self.cursor
        dx = DIRECTIONS[direction][0] * 5 if mod else DIRECTIONS[direction][0]
        dy = DIRECTIONS[direction][1] * 5 if mod else DIRECTIONS[direction][1]
        nx, ny = x + dx, y + dy
        if self.engine.world.area.in_bounds(nx, ny):
            self.set_cursor(nx, ny)

    def render(self, console):

        # Render the parent
        self.parent.render(console)

        # Render the overlay menu
        self.render_cursor(console)

    def render_cursor(self, console):
        """Highlight the currently-selected tile."""
        console.tiles_rgb["bg"][self.cursor[0],
                                self.cursor[1]] = C["WHITE"]
        console.tiles_rgb["fg"][self.cursor[0],
                                self.cursor[1]] = C["BLACK"]

    @property
    def target(self):
        """Generate the target object."""
        raise NotImplementedError()

    def resume(self):
        """Return control to the parent state."""

        self.engine.set_state(self.parent)

    def resume_with_selection(self):
        """Return control to the parent state, passing back a decision."""

        # Return to the previous state
        self.resume()

        # Pass an action to be handled
        self.engine.state.handle_event(self.target)

    def ev_keydown(self, event):
        """Take keyboard input."""

        # Get event information
        key = event.sym
        mod = True if event.mod and tcod.event.KMOD_LSHIFT else False

        if key == tcod.event.K_UP:
            self.move_cursor("UP", mod)

        elif key == tcod.event.K_DOWN:
            self.move_cursor("DOWN", mod)

        elif key == tcod.event.K_LEFT:
            self.move_cursor("LEFT", mod)

        elif key == tcod.event.K_RIGHT:
            self.move_cursor("RIGHT", mod)

        elif key == tcod.event.K_RETURN:
            self.resume_with_selection()

        elif key == tcod.event.K_ESCAPE:
            self.resume()

    def ev_mousebuttondown(self, event):
        """Selects on mouse click."""
        if self.engine.world.area.in_bounds(*self.cursor):
            self.resume_with_selection()


class LookState(TargetState):

    def __init__(self, engine, parent):
        super().__init__(engine, parent)

    @property
    def target(self):
        """On confirmation, return to the game."""
        return None


class ThrowState(TargetState):

    def __init__(self, engine, parent, thrower, item):
        super().__init__(engine, parent)
        self.thrower = thrower
        self.item = item

    @property
    def target(self):
        """On confirmation, return to the game."""
        return Throw(self.item, self.cursor)

    def move_cursor(self, direction, mod):
        """Move the cursor in a particular direction;
        bound by the map and the thrower's strength"""
        x, y = self.cursor
        dx = DIRECTIONS[direction][0] * 5 if mod else DIRECTIONS[direction][0]
        dy = DIRECTIONS[direction][1] * 5 if mod else DIRECTIONS[direction][1]
        nx, ny = x + dx, y + dy

        # If the tile is valid
        if self.engine.world.area.in_bounds(nx, ny):

            # And not further than the thrower can throw
            dist = self.engine.world.area.distance_between((nx, ny),
                                                           self.thrower.loc)

            # Highlight it
            if dist <= self.thrower.body.strength:
                self.set_cursor(nx, ny)

    def render_impact_radius(self, console):
        """Highlight the tiles that would be affected by the impact."""

        # Get the tiles in the area
        tiles = self.thrower.area.get_tiles_in_range(self.cursor[0],
                                                     self.cursor[1],
                                                     self.item.impact_radius)

        # Remove the impact tile
        tiles.remove(self.cursor)

        # Highlight each tile
        for tile in tiles:
            console.tiles_rgb["bg"][tile[0],
                                    tile[1]] = C["WHITE"]
            console.tiles_rgb["fg"][tile[0],
                                    tile[1]] = C["BLACK"]

    def render_cursor(self, console):
        console.tiles_rgb["bg"][self.cursor[0],
                                self.cursor[1]] = C["WHITE"]
        console.tiles_rgb["fg"][self.cursor[0],
                                self.cursor[1]] = C["BLACK"]

        if hasattr(self.item, "impact_radius"):
            self.render_impact_radius(console)
