"""Entry point for the game."""

from components.utility.engine import Engine


def main():

    # Variable set up - to be extracted later
    width = 80
    height = 60
    tileset = "./assets/arial12x12.png"

    # Create the game object
    game = Engine(width, height, tileset)

    # Begin the loop
    game.start_main_loop()


if __name__ == "__main__":
    main()
