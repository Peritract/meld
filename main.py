"""Entry point for the game."""

from components.utilities.engine import Engine


def main():

    # Variable set up - to be extracted later
    title = "Working Title"
    width = 80
    height = 60
    tileset = "./assets/arial12x12.png"

    # Create the game object
    game = Engine(title, width, height, tileset)

    # Begin the loop
    game.run_main_loop()


if __name__ == "__main__":
    main()
