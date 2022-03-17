from file_io import read_json
from pysweeper import Pysweeper


def main():
    game_settings = read_json("data/config.json")
    game = Pysweeper(game_settings["width"],
                     game_settings["height"],
                     game_settings["bombs"])
    game.run()


if __name__ == "__main__":
    main()
