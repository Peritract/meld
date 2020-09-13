"""This class contains the implementation of the Brawler
AI; this attacks the player without restraint."""

from .mind import Mind
from ..actions import Wait, Move, Attack


class Brawler(Mind):
    """Attacks the player, if possible."""

    def __init__(self):
        super().__init__()
        self.target = None
        self.last_known_target = None

    def make_decision(self):
        """Selects a target and moves towards it."""

        # Clear the target
        self.target = None

        # If at the last known position of a target,
        if self.last_known_target == (self.owner.x, self.owner.y):
            # clear the position
            self.last_known_target = None

        # Calculate the entity's field of view
        visible = self.area.calculate_fov(self.owner)

        # Search the entity list for a visible & attackable one
        # Currently just attacks the player - further functionality planned
        for entity in self.area.entities:
            if visible[entity.x, entity.y] and entity.faction == "player":

                # Set the target, and its last known location
                self.target = entity
                self.last_known_target = (self.target.x, self.target.y)

        # If no target is visible and no position is logged, do nothing
        if not self.target and not self.last_known_target:
            return Wait()

        # Calculate the next step towards the goal
        goal = (self.target.x,
                self.target.y) if self.target else self.last_known_target
        path = self.area.get_path_to(self.owner, goal[0], goal[1])

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
            # If it's close enough to attack,
            if next_step == [self.target.x, self.target.y]:
                # Attack
                return Attack(self.target)

        # If possible, move towards the goal
        if not self.area.get_blocker_at_location(next_step[0], next_step[1]):
            return Move(direction[0], direction[1])

        # In all other situations, just wait
        return Wait()
