"""This file contains the implementations of the various body parts;
Each organ/limb has different stat effects or grants different abilities.
"""

from .body import Eyes


class HumanEyes(Eyes):
    """Totally normal human eyes."""

    def __init__(self):
        super().__init__("eyes", "normal human eyes", 5)


class Eyestalks(Eyes):
    """Snail eyes on tentacles."""

    def __init__(self):
        super().__init__("eyestalks", "soft eye-tipped tentacles", 3)
