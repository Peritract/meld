"""
This file contains the implementations of the various
AI "minds" - the logic for how each entity acts & takes turns.
"""

from ..utility.event_handlers import PlayerEventHandler
from ..utility.actions import Surge, Move, Attack, Wait
from ..utility.point import Point
import tcod.event
import tcod.path
from random import choice
import numpy as np


class Mind():
    """The base mind class."""

    def take_action(self, level):
        # Generic turn-taking function
        print('The ' + self.owner.name + ' moves in mysterious ways.')

    def get_tile_cost(self, level):
        """Calculate the cost of movement around the level."""

        # Make a copy of the passable map
        cost = np.array(level.tiles["passable"], dtype=np.int8)

        # Squares containing entities have a higher cost
        # - discourage routing through them
        for entity in level.entities:
            if entity.blocks and cost[entity.x, entity.y]:
                cost[entity.x, entity.y] += 10

        # Return the cost map
        return cost

    def get_path_to(self, other, level):
        """Finds a route to another object."""

        # Get the cost map
        cost = self.get_tile_cost(level)

        # Convert the map to a graph (disallow diagonal movement)
        graph = tcod.path.AStar(cost=cost, diagonal=0)

        # Find a path if possible
        path = graph.get_path(self.owner.x, self.owner.y, other.x, other.y)

        # If movement is possible
        if path:
            # Return all the path except the starting point
            return path[1:]
        else:
            # No path can be found
            return None


class Wanderer(Mind):
    """Moves randomly, with no awareness."""

    def take_action(self, level):

        # Makes a choice - move or not
        move = choice([True, False])

        if not move:
            # Do nothing
            return Wait()
        else:
            # Choose a random possible direction and move in it

            # Get a list of adjacent spaces
            directions = level.get_adjacent_spaces(self.owner.x, self.owner.y)

            # Filter out occupied spaces
            directions = [x for x in directions
                          if not
                          level.get_blocking_entity(self.owner.x + x[0],
                                                    self.owner.y + x[1])]

            # Return a movement action to a random, unoccupied space
            return Move(*choice(directions))


class Player(Mind):
    """The mind class for a player-controlled character."""

    def __init__(self):
        self.event_handler = PlayerEventHandler()

    def take_action(self, level):

        # Start a loop until a turn-ending action
        complete = False

        while not complete:
            # Take user input
            for event in tcod.event.wait():

                # Check the event against valid actions
                decision = self.event_handler.dispatch(event)

                # Ignore invalid actions
                if not decision:
                    continue

                # If the action has a direction,
                if isinstance(decision, Surge):

                    # Check that the direction is valid
                    new_x = self.owner.x + decision.dx
                    new_y = self.owner.y + decision.dy
                    if not level.in_bounds(new_x, new_y) or \
                       not level.is_passable(new_x, new_y):
                        continue

                    # If there is an entity in the way
                    entity = level.get_blocking_entity(new_x, new_y)
                    if entity:
                        decision = Attack(decision.dx, decision.dy, entity)

                    # Otherwise
                    else:
                        decision = Move(decision.dx, decision.dy)

                # Check if the action ends the turn
                complete = decision.final

                # If the action completes, jump out of the for loop
                if complete:
                    break

        # Now a valid, turn-ending input has been found, return it.
        return decision


class Hunter(Mind):
    """Attacks the player if possible."""

    def __init__(self):
        super().__init__()
        self.target = None
        self.last_known_target = None

    def take_action(self, level):
        """Selects a target and moves towards it."""

        # Clear the target
        self.target = None
        # If at the last known position of a target,
        if self.last_known_target == Point(self.owner.x, self.owner.y):
            # clear the position
            self.last_known_target = None

        # Calculate the entity's field of view
        visible = level.get_fov(self.owner)

        # Search the entity list for a visible & attackable one
        # Currently just attacks the player - further functionality planned
        for entity in level.entities:
            if visible[entity.x, entity.y] and entity.faction == "player":

                # Set the target, and its last known location
                self.target = entity
                self.last_known_target = Point(self.target.x, self.target.y)

        # If no target is visible and no position is logged, do nothing
        if not self.target and not self.last_known_target:
            return Wait()

        # Calculate the next step towards the goal
        goal = self.target if self.target else self.last_known_target
        path = self.get_path_to(goal, level)

        # If there is a path
        if path:
            # Grab the next point on it
            next_step = path[0]
        else:
            # Otherwise just pause
            return Wait()

        # Calculate the movement required
        direction = (next_step[0] - self.owner.x,
                     next_step[1] - self.owner.y)

        # If the target is in view
        if self.target:
            print("Seen!")
            # If it's close enough to attack,
            if next_step == (self.target.x, self.target.y):
                # Attack
                return Attack(direction[0],
                              direction[1],
                              self.target)

        # If possible, move towards the goal
        if not level.get_blocking_entity(next_step[0], next_step[1]):
            return Move(direction[0], direction[1])

        # In all other situations, just wait
        return Wait()
