from file_io import read_json
from pysweeper import Pysweeper
from sprites import load_file


def main() -> None:
    game_settings = read_json(load_file("data/config.json"))
    game = Pysweeper(game_settings["width"],
                     game_settings["height"],
                     game_settings["bombs"],
                     game_settings["jr_reveal"])
    game.run()


if __name__ == "__main__":
    main()
