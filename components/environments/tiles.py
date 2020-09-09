"""This file contains the various tile datatypes."""

import numpy as np

# Struct for tile appearance information
# Character (as int - ord()), foreground colour (3 bytes) and background

tile_appearance = np.dtype([("char", np.int32),
                            ("fg", "3B"),
                            ("bg", "3B")])

# Struct for tile information

tile_type = np.dtype([("passable", np.bool),
                      ("transparent", np.bool),
                      ("out_of_view", tile_appearance),
                      ("in_view", tile_appearance)])

# Unknown/unseen tile

unknown = np.array((ord(" "),
                   (255, 255, 255),
                   (0, 0, 0)),
                   dtype=tile_appearance)

# Basic floor tile

basic_floor = np.array((True, True,
                        np.array((ord(" "),
                                 (255, 255, 255),
                                 (50, 50, 150)),
                                 dtype=tile_appearance),
                        np.array((ord(" "),
                                 (255, 255, 255),
                                 (200, 180, 50)),
                                 dtype=tile_appearance)),
                       dtype=tile_type)

# Basic wall

basic_wall = np.array((False, False,
                      np.array((ord(" "),
                               (255, 255, 255),
                               (0, 0, 150)),
                               dtype=tile_appearance),
                      np.array((ord(" "),
                               (255, 255, 255),
                               (130, 110, 50)),
                               dtype=tile_appearance)),
                      dtype=tile_type)
