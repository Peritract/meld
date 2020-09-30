"""This file contains the implementation of the TargetState class
and its subclasses; these classes allow the user to select a given
in-game tile.
"""

from .state import State
from ..constants import DIRECTIONS, COLOURS as C
from ...entities.actions import Throw, Fire
import tcod
from .text_states import OverlayText


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

    @property
    def target(self):
        """Generate the target object."""
        raise NotImplementedError()

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
        self.highlight_tile(self.cursor[0], self.cursor[1],
                            console, C["TARGET"])

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

    def highlight_tile(self, x, y, console, colour=C["PATH"]):
        """Highlight a tile."""
        console.tiles_rgb["bg"][x, y] = colour
        console.tiles_rgb["fg"][x, y] = C["BLACK"]


class LookState(TargetState):

    def __init__(self, engine, parent):
        super().__init__(engine, parent)

    def get_tile_details(self):
        """Get the descriptions of tile contents."""

        # Get tile contents at the cursor
        contents = self.engine.world.area.at_location(*self.cursor)

        # Extract the interesting bits
        if contents:
            contents = [x.description for x in contents]

        return contents

    def create_pop_up(self):
        """Create a pop-up of descriptions at the cursor."""

        if self.engine.world.area.is_visible(*self.cursor):
            descriptions = self.get_tile_details()

            # Join the descriptions into a solid block of text
            text = "\nBLANK\n".join(descriptions)

            # Create and display the pop-up
            state = OverlayText(self.engine, self, self.parent, text)
            self.engine.set_state(state)

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
            self.create_pop_up()

        elif key == tcod.event.K_ESCAPE:
            self.resume()

    def ev_mousebuttondown(self, event):
        """Selects on mouse click."""
        if self.engine.world.area.in_bounds(*self.cursor):
            self.create_pop_up()


class RangeState(TargetState):
    """Allows the user to a select a tile within a range in a direct line
    from the player entity."""

    def __init__(self, engine, parent, actor, projectile, range):
        super().__init__(engine, parent)
        self.actor = actor
        self.projectile = projectile
        self.range = range

    @property
    def target(self):
        """The selected choice."""
        raise NotImplementedError()

    def calculate_projectile_path(self):
        """Identify the point of impact, based on the range."""

        if self.actor.loc == self.cursor:
            # Return the actor's location and an empty path
            return self.cursor, []

        # Get the direct route to the target
        path = self.actor.area.get_direct_path_to(self.actor.loc,
                                                  self.cursor)[1:]

        # Move the item along the path as far as the range
        # or until it hits something
        in_motion = True
        impact_point = self.actor.loc
        step = 0

        # Holder for the path travelled
        line = []

        while in_motion:
            curr = tuple(path[step])
            impact_point = curr
            dist = self.engine.world.area.distance_between(self.actor.loc,
                                                           curr)
            # If it's travelled as far as strength or has hit something
            if dist >= self.range or not self.actor.area.is_passable(*curr) \
                    or self.actor.area.get_blocker_at_location(*curr) or \
                    len(path) - 1 <= step:
                in_motion = False
                # If it has hit a wall, go back one to avoid weird edge cases
                if not self.engine.world.area.is_passable(*curr):
                    impact_point = tuple(path[step - 1])
            else:
                line.append(curr)
                step += 1

        # Return the impact point and the path to it
        return impact_point, line

    def move_cursor(self, direction, mod):
        """Move the cursor in a particular direction with the keys;
        bound by the map and the range"""
        x, y = self.cursor
        dx = DIRECTIONS[direction][0] * 5 if mod else DIRECTIONS[direction][0]
        dy = DIRECTIONS[direction][1] * 5 if mod else DIRECTIONS[direction][1]
        nx, ny = x + dx, y + dy

        # If the tile is valid
        if self.engine.world.area.in_bounds(nx, ny):
            self.set_cursor(nx, ny)

    def render_impact_radius(self, console):
        """Highlight the tiles that would be affected by the impact."""

        # Get the tiles in the area
        radius = self.projectile.impact_radius
        tiles = self.engine.world.area.get_tiles_in_range(self.impact[0],
                                                          self.impact[1],
                                                          radius)

        # Highlight each tile
        for tile in tiles:
            self.highlight_tile(tile[0], tile[1], console, C["RADIUS"])

    def render_cursor(self, console):

        # Work out where the item will hit
        self.impact, line = self.calculate_projectile_path()

        # Highlight the steps along the path
        for step in line:
            self.highlight_tile(step[0], step[1], console)

        # If the projectile will affect an area
        if hasattr(self.projectile, "impact_radius"):

            # Highlight the area
            self.render_impact_radius(console)

        # Highlight the impact tile
        self.highlight_tile(self.impact[0], self.impact[1],
                            console, C["TARGET"])


class ThrowState(RangeState):
    """Throw an object."""

    def __init__(self, engine, parent, actor, item):
        super().__init__(engine, parent, actor, item,
                         actor.body.throw_range)

    @property
    def target(self):
        """The selected choice."""
        return Throw(self.projectile, self.impact)


class FireState(RangeState):
    """Fire a projectile."""

    def __init__(self, engine, parent, actor, projectile, fire_range):
        super().__init__(engine, parent, actor, projectile, fire_range)

    @property
    def target(self):
        """The selected choice."""
        return Fire(self.projectile, self.impact)
