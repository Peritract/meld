"""This file contains the implementation of the various
conditions, such as poison."""


from ..utilities.messages import AlertMessage
from ..entities.minds.seeker_mind import Seeker


class Condition:
    """A temporary status condition."""

    def __init__(self, duration, target):
        self.duration = duration
        self.target = target

        self.attach()

    def attach(self):
        """Change the target when attached."""
        pass

    def remove(self):
        """Undo changes when removed."""

        # Break the link
        self.target.conditions.remove(self)
        self.target = None

    def apply(self):
        """Affect the target."""
        pass

    def update(self):
        """Count down, applying any turn-based effect."""

        # Have an effect
        self.apply()

        # Count down
        self.duration -= 1

        # If the duration has run out, remove it
        if self.duration <= 0:

            # Remove the condition
            self.remove()


class Poison(Condition):
    """Reduce health each turn."""

    def __init__(self, duration, damage, target):
        super().__init__(duration, target)
        self.damage = damage

    def apply(self):
        """Subtract health."""

        verb = "is" if self.target.faction != "player" else "are"
        text = f"{self.target.phrase} {verb} damaged by poison."
        self.target.area.post(AlertMessage(text))
        self.target.body.take_damage(self.damage)


class Lure(Condition):
    """Move towards danger."""

    def __init__(self, duration, target, goal):
        self.goal = goal
        self.mind = Seeker(self.goal)
        super().__init__(duration, target)

    def attach(self):
        """Replace target mind with Seeker mind."""

        text = f"{self.target.phrase} is entranced!"
        self.target.area.post(AlertMessage(text))
        self.normal_state = self.target.mind
        self.target.mind = self.mind
        self.target.mind.owner = self.target

    def remove(self):
        text = f"{self.target.phrase} is no longer entranced!"
        self.target.area.post(AlertMessage(text))
        self.target.mind = self.normal_state
        self.mind.owner = None
        super().remove()
