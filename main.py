"""Entry point for the game."""

from components.engine import Engine


def main():

    # Variable set up - to be extracted later
    width = 50
    height = 50
    tileset = "./assets/arial12x12.png"

    # Create the game object
    game = Engine(width, height, tileset)

    # Begin the loop
    game.start_main_loop()


if __name__ == "__main__":
    main()
