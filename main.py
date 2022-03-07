from pysweeper import Pysweeper

# https://minesweeperonline.com/


def main():
    game = Pysweeper(20, 20, 40)
    game.run()


if __name__ == "__main__":
    main()
