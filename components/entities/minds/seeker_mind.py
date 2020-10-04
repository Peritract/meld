"""This class contains the implementation of the Seeker
AI; this moves towards a specific tile."""

from .mind import Mind
from ..actions import Wait, Move


class Seeker(Mind):
    """Moves towards the tiles."""

    def __init__(self, target):
        super().__init__()
        self.target = target

    def make_decision(self):
        """Moves towards the target if possible."""

        # Calculate the entity's field of view
        visible = self.area.calculate_fov(self.owner)

        # Check that the target is visible
        if not visible[self.target.x, self.target.y]:
            return Wait()

        # Calculate the next step towards the goal
        goal = self.target.loc
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

        # If possible, move towards the goal
        if not self.area.get_blocker_at_location(next_step[0], next_step[1]):
            return Move(direction[0], direction[1])

        # In all other situations, just wait
        return Wait()
