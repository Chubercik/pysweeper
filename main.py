from random import randint


def create_a_board(width, heigth):
    board = []
    for line in range(heigth):
        board.append([])
        for _ in range(width):
            board[line].append(0)
    return board


def scatter_bombs(board):
    for line in range(len(board)):
        for tile in range(len(board[line])):
            rand_num = randint(1, 100)
            if 75 < rand_num <= 100:
                board[line][tile] = 'X'


def main():
    board = create_a_board(5, 4)
    scatter_bombs(board)
    print(board)


if __name__ == "__main__":
    main()
