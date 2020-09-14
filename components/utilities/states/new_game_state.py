"""
This class contains the implementation of the NewGameState class.
This class creates and populates the game world.
"""

from .state import State

# -- HACK -- #

from ...entities.entity import Entity
from ...entities.player_entity import Player
from ...environments.world import World
from ...environments.area import Area
from ...environments.tiles import basic_wall
from ...entities.minds.wanderer_mind import Wanderer
from ...entities.minds.brawler_mind import Brawler

from ..message_log import MessageLog, Message

# -- /HACK -- #


class NewGameState(State):
    """Creates and populates the game world."""

    def __init__(self, engine):
        super().__init__(engine)

    def handle_events(self, window):
        """Doesn't actually handle events; calls the creation scripts."""

        # Clean up from previous games
        self.clean_up()

        # Create the world
        self.create_world()

        # Change the state
        self.engine.set_state("play_game")

    def clean_up(self):
        """Deals with loose ends from potential previous games."""
        self.engine.message_log = MessageLog()

    def create_world(self):
        """Creates a new game world."""
        world = World(self.engine)
        self.engine.world = world
        area = Area(80, 50, self.engine.world)
        self.engine.player = Player("player", 5, 5, area=area)
        other = Entity("other", 10, 10, mind=Wanderer, area=area)
        enemy = Entity('enemy', 15, 15, mind=Brawler, area=area)
        area.tiles[30:33, 22] = basic_wall
        self.engine.message_log.add_message(Message("I am alive!"))
        world.areas.append(area)
        world.current_area = 0
        world.area.contents = world.area.contents.union({self.engine.player,
                                                         other,
                                                         enemy})
        