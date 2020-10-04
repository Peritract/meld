"""This file contains the implementations of the various body parts;
Each organ/limb has different stat effects or grants different abilities.
"""


class Part:
    """A generic body part."""

    def __init__(self, name):
        self.name = name


class Manipulator(Part):
    """An arm, tentacle, or otherwise, used for interaction."""

    def __init__(self, name):
        super().__init__(name)


class Transporter(Part):
    """A leg/tail/tentacle used for movement."""

    def __init__(self, name):
        super().__init__(name)


class Skin(Part):
    """The thing covering everything else."""

    def __init__(self, name):
        super().__init__(name)


class Mouth(Part):
    """Mostly for biting."""

    def __init__(self, name):
        super().__init__(name)


class Trunk(Part):
    """The central part of the body."""

    def __init__(self, name):
        super().__init__(name)


class Eye(Part):
    """Sensory organ."""

    def __init__(self, name):
        super().__init__(name)
