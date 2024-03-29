"""This file contains the implementations of the various body parts;
Each organ/limb has different stat effects or grants different abilities.
"""

from ..abilities import AcidSpit

class Part:
    """A generic body part."""

    def __init__(self, name, desc, affinity='human', type=None):
        self.name = name
        self.desc = desc
        self.affinity = affinity
        self.type = type
        self.prerequisites = None

    def __repr__(self):
        return f"body part ({self.name})"

## Eyes

class Eyes(Part):
    """Sensory organ."""

    def __init__(self, name, desc, view_radius, affinity='human'):
        super().__init__(name, desc, affinity, type="eyes")
        self.view_radius = view_radius


class HumanEyes(Eyes):
    """Totally normal human eyes."""

    def __init__(self):
        super().__init__("eyes", "normal human eyes", 5, affinity='human')


class Eyestalks(Eyes):
    """Snail eyes on tentacles."""

    def __init__(self):
        super().__init__("eyestalks", "soft eye-tipped tentacles", 3,
                         affinity='snail')

## Arms

class Manipulators(Part):
    """Grasping limbs/pseudopods/similar"""

    def __init__(self, name, desc, can_equip, verb='flail', damage=1, strength=5, affinity='human'):
        super().__init__(name, desc, affinity, type="manipulators")
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
        super().__init__("small crab claws", "small clutching claws", can_equip=False, verb="snip",
                         damage=2, strength=4, affinity='crab')

## Legs

class Propulsors(Part):
    """Limbs and such for locomotion."""

    def __init__(self, name, desc, speed=10, affinity='human'):
        super().__init__(name, desc, affinity, type="propulsors")
        self.speed = speed


class HumanLegs(Propulsors):
    """Normal human legs and feet."""

    def __init__(self):
        super().__init__("legs", "normal human legs and feet", speed=10, affinity='human')

class CrabLegs(Propulsors):
    """Normal human legs and feet."""

    def __init__(self):
        super().__init__("crab legs", "six chitinous, segmented limbs", speed=10, affinity='crab')

## Skin

class Exterior(Part):
    """Flesh and carapaces."""

    def __init__(self, name, desc, max_health=10, defence=0, affinity='human'):
        super().__init__(name, desc, affinity, type="exterior")
        self.max_health = max_health
        self.defence = defence

    def on_contact(self, other):
        pass


class HumanSkin(Exterior):
    """Normal human skin."""

    def __init__(self):
        super().__init__("skin", "normal human skin", max_health=10, defence=0, affinity='human')


class ThinCrabShell(Exterior):
    """First level of crab defence."""

    def __init__(self):
        super().__init__("shell", "thin crab shell", max_health=10, defence=5, affinity='crab')
        self.article = "a"

# Mouths

class Mouth(Part):
    """Biting and spitting."""
    def __init__(self, name, desc, affinity='human'):
        super().__init__(name, desc, affinity, type="mouth")

    def on_contact(self, other):
        pass
    

class HumanMouth(Mouth):
    """Normal human mouth."""
    def __init__(self):
        super().__init__(name="mouth", desc="normal human mouth", affinity="human")
        self.article = "a"


class AcidSpittingMouth(Mouth):
    """Spit acid."""
    def __init__(self, name="acid-spitting mouth", desc="acid-spitting mouth", affinity='toad'):
        super().__init__(name, desc, affinity)
        self.article = "an"
        self.ability = AcidSpit()

    def on_contact(self, other):
        pass

# Collection of all possible parts

parts = [HumanEyes, HumanHands, HumanLegs, HumanSkin, HumanMouth,
         Eyestalks, SmallCrabClaws, ThinCrabShell, AcidSpittingMouth,
         CrabLegs]