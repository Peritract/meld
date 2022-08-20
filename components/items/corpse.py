"""This file contains the implementation of the Corpse class."""

from .items import Consumable
from ..utilities.constants import COLOURS as C
from ..utilities.exceptions import Impossible
from ..utilities.messages import AlertMessage

class Corpse(Consumable):

    def __init__(self, name="body", x=0, y=0, area=None, health=2, affinities={}):
        super().__init__(name="Corpse", 
                         description=f"A dead {name}.",
                         verb='consume', uses=1,
                         x=x, y=y, char="%",
                         colour=C["GREY"], area=area)
        self.health = health
        self.affinities = affinities

    @property
    def description_text(self):
        return self.description

    def affect(self, target):
        """Heals the target."""
        if target.body.health < target.body.max_health:
            target.body.heal(self.health)
            
            if target.faction == 'player':
                text = "You are revitalised!"
            else:
                text = f"{target.phrase} is revitalised!"
            target.area.post(AlertMessage(text))
            
        # Eating corpses of specific creature affinities makes you more likely to mutate into those sorts of creature.
        target.body.increase_affinities(self.affinities)

        # Consuming tainted flesh makes you more likely to mutate.
        target.body.instability += 10