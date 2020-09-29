"""This file contains the implementation of the various
conditions, such as poison."""


from ..utilities.messages import AlertMessage


class Condition:
    """A temporary status condition."""

    def __init__(self, duration):
        self.duration = duration

    def attach(self, target):
        """Change the target when attached."""
        self.target = target

    def remove(self):
        """Undo changes when removed."""

        # Break the link
        self.target.conditions.remove(self)
        self.target = None

    def apply(self):
        """Affect the target."""
        pass

    def act(self):
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

    def __init__(self, duration, damage):
        super().__init__(duration)
        self.damage = damage

    def apply(self):
        """Subtract health."""

        verb = "is" if self.target.faction != "player" else "are"
        text = f"{self.target.phrase} {verb} damaged by poison."
        self.target.area.post(AlertMessage(text))
        self.target.body.take_damage(self.damage)
