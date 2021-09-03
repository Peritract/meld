"""This file contains the implementations of the various body parts;
Each organ/limb has different stat effects or grants different abilities.
"""

class Part:
    """A generic body part."""

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc


class Eyes(Part):
    """Sensory organ."""

    def __init__(self, name, desc, view_radius):
        super().__init__(name, desc)
        self.view_radius = view_radius


class HumanEyes(Eyes):
    """Totally normal human eyes."""

    def __init__(self):
        super().__init__("eyes", "normal human eyes", 5)


class Eyestalks(Eyes):
    """Snail eyes on tentacles."""

    def __init__(self):
        super().__init__("eyestalks", "soft eye-tipped tentacles", 3)


class Manipulators(Part):
    """Grasping limbs/pseudopods/similar"""

    def __init__(self, name, desc, can_equip, verb='flail', damage=1, strength=5):
        super().__init__(name, desc)
        self.can_equip = can_equip
        self.verb = verb
        self.damage = damage
        self.strength = strength


class HumanHands(Manipulators):
    """Normal human arms and hands."""

    def __init__(self):
        super().__init__("hands", "normal human arms and hands", can_equip=True, verb="strike", damage=1, strength=5)


class SmallCrabClaws(Manipulators):
    """Small, clutching claws."""

    def __init__(self):
        super().__init__("small crab claws", "small clutching claws", can_equip=False, verb="snip", damage=1, strength=4)


class Propulsors(Part):
    """Limbs and such for locomotion."""

    def __init__(self, name, desc, speed=10):
        super().__init__(name, desc)
        self.speed = speed


class HumanLegs(Propulsors):
    """Normal human legs and feet."""

    def __init__(self):
        super().__init__("legs", "normal human legs and feet", speed=10)