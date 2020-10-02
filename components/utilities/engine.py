"""
This file implements the engine class;
An instance of this class manages the
game screen and states.
"""

import tcod
from .states.main_menu_state import MainMenu
from .states.game_over_state import GameOver
from .messages import WorldMessage, MessageLog
import pickle
import lzma

# -- HACK -- #

from ..entities.entity import Entity
from ..entities.player_entity import Player
from ..environments.world import World
from ..environments.area import Area
from ..environments.tiles import basic_wall
from ..entities.minds.wanderer_mind import Wanderer
from ..entities.minds.brawler_mind import Brawler
from ..items.corpse import Corpse
from ..items.consumables import Bandage, AcidFlask
from ..items.equippables import Cudgel, Robe, VenomDagger
from ..utilities.states.play_state import Play
from ..environments.features import Stairs
from ..entities.abilities import AcidSpit

# -- /HACK -- #


class Engine:
    """Manages the game screen and states."""

    def __init__(self, screen_title, screen_width, screen_height, font):
        """Sets key variables."""

        # Screen appearance
        self.screen_title = screen_title
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.tileset = tcod.tileset.load_tilesheet("./assets/arial12x12.png",
                                                   32, 8,
                                                   tcod.tileset.CHARMAP_TCOD)

        # Drawing console
        # Order=F flips x and y, for easier drawing
        self.console = tcod.Console(self.screen_width, self.screen_height,
                                    order="F")

        # Starting state
        self.state = MainMenu(self)

        # Mouse location
        self.m_loc = (0, 0)

        # Message storage
        self.message_log = MessageLog()

    def set_state(self, state):
        """Changes the engine state."""
        self.state = state

    def new_game(self):
        """Creates a new game world and then switches the state to playing."""

        # Clean up after any previous game
        self.clean_up()

        self.create_world()
        self.set_state(Play(self))

    def save_game(self):
        """Saves the current state of the game world and
        then switches to the main menu."""

        # Unhook the world from the engine
        self.world.engine = None

        # Pickle and compress the data
        data = lzma.compress(pickle.dumps(self.world))

        # Write the data to the savefile
        with open("savefile.sav", "wb") as file:
            file.write(data)

        # Go back to the menu
        self.set_state(MainMenu(self))

    def load_game(self):
        """Load a game from a file and then switches the state to playing."""

        # Clean up after any previous game
        self.clean_up()

        # Open the save file
        with open("savefile.sav", "rb") as file:

            # Load the data
            data = pickle.loads(lzma.decompress(file.read()))

        # Hook it all back up together
        self.world = data
        self.world.engine = self

        # Resume playing
        self.set_state(Play(self))

    def game_over(self):
        """Ends the game."""
        self.state = GameOver(self, self.state)

    def clean_up(self):
        """Clears things that would otherwise persist in between games."""
        self.message_log = MessageLog()

    def run_main_loop(self):
        """Repeatedly calls the current state method."""

        # Make the window
        """Creates the main window and begins the game loop."""
        with tcod.context.new_terminal(self.screen_width,
                                       self.screen_height,
                                       tileset=self.tileset,
                                       title=self.screen_title) as window:

            # Flag for the game running
            while True:

                # Clear the window
                self.console.clear()

                # Render the current state
                self.state.render(self.console)

                # Flush the console to the window
                window.present(self.console)

                # Call the current state's event handler
                self.state.handle_events(window)

# -- HACK -- #

    def create_world(self):
        """Creates a new game world."""
        world = World(self)
        self.world = world
        area = Area(80, 50, world, "surface")
        area2 = Area(80, 50, world, "caverns", 1)
        player = Player("Player", "A person", 5, 5)
        world.player = player
        other = Entity("other", "Not you.", 10, 10, mind=Wanderer)
        enemy = Entity('enemy', "A horror", 15, 15, mind=Brawler)
        A, B, C = Corpse("A", 1, 1), Corpse("B", 1, 1), Corpse("C", 2, 2)
        D, E, F = Bandage(3, 3), Cudgel(4, 4), Robe(6, 6)
        G = AcidFlask(7, 7)
        area.tiles[30:33, 22] = basic_wall
        self.message_log.add(WorldMessage("Your journey begins."
                                          "You are unlikely to survive"))
        world.areas.append(area)
        world.areas.append(area2)
        world.area.add_contents([player, other, enemy,
                                 A, B, C, D, E])
        area2.add_contents(Stairs(6, 6, area2, area))
        area.add_contents(Stairs(10, 10, area, area2))
        other.pick_up(G)
        enemy.pick_up(F)
        player.pick_up(AcidFlask())
        player.pick_up(VenomDagger())
        player.add_ability(AcidSpit())
        h = []
        for x in range(10, 30):
            for y in range(10, 30):
                h.append(Entity("other", "Not you.", x, y, mind=Wanderer))
        area2.add_contents(h)

# -- /HACK -- #
