import random


class Isolation:
    """Isolation is a class that implements the isolation game.
    """
    def __init__(self, player1, player2):
        """Initialize the game with two players.
        """
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.board = self.get_empty_board()
        self.player1_score = 0
        self.player2_score = 0
        self.move_count = 0

    def get_empty_board(self):
        """Return a list of lists representing an empty board.
        """
        return [[' ' for _ in range(3)] for _ in range(3)]

    def get_possible_moves(self):
        """Return a list of possible moves.
        """
        moves = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    moves.append((row, col))
        return moves

    def make_move(self, row, col):
        """Make a move on the board.
        """
        self.board[row][col] = self.current_player.mark
        self.move_count += 1
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def is_winner(self):
        """Return True if the current player has won.
        """
        if self.board[0][0] == self.current_player.mark and \
                self.board[0][1] == self.current_player.mark and \
                self.board[0][2] == self.current_player.mark:
            return True
        elif self.board[1][0] == self.current_player.mark and \
                self.board[1][1] == self.current_player.mark and \
                self.board[1][2] == self.current_player.mark:
            return True
        elif self.board[2][0] == self.current_player.mark and \
                self.board[2][1] == self.current_player.mark and \
                self.board[2][2] == self.current_player.mark:
            return True
        elif self.board[0][0] == self.current_player.mark and \
                self.board[1][0] == self.current_player.mark and \
                self.board[2][0] == self.current_player.mark:
            return True
        elif self.board[0][1] == self.current_player.mark and \
                self.board[1][1] == self.current_player.mark and \
                self.board[2][1] == self.current_player.mark:
            return True
        elif self.board[0][2] == self.current_player.mark and \
                self.board[1][2] == self.current_player.mark and \
                self.board[2][2] == self.current_player.mark:
            return True
        elif self.board[0][0] == self.current_player.mark and \
                self.board[1][1] == self.current_player.mark and \
                self.board[2][2] == self.current_player.mark:
            return True
        elif self.board[0][2] == self.current_player.mark and \
                self.board[1][1] == self.current_player.mark and \
                self.board[2][0] == self.current_player.mark:
            return True
        else:
            return False

    def move(self, row, col):
        """Make a move on the board.
        """
        self.make_move(row, col)

    def turn(self):
        if self.move_count % 2 == 0:
            return "player1"
        else:
            return "player2"

    def play(self):
        """Play the game.
        """
        while not self.is_winner():
            self.current_player.move(self)
            if self.is_winner():
                if self.current_player == self.player1:
                    self.player1_score += 1
                else:
                    self.player2_score += 1
            self.current_player = self.player1 if self.current_player == \
                self.player2 else self.player2

            print(self)
            print("Player 1: {}".format(self.player1_score))
            print("Player 2: {}".format(self.player2_score))

    def __str__(self):
        """Return a string representation of the board.
        """
        return ''.join('|'.join(row) + '\n' for row in self.board)


class HumanPlayer:
    """Player that chooses moves on the command line.
    """
    def __init__(self):
        self.mark = 'X'

    def get_move(self, game):
        """Get a move from the user.
        """
        print("Enter a move: ")
        return input()

    def move(self, game):
        """Make a move on the board.
        """
        move = self.get_move(game)
        row, col = move.split()
        row, col = int(row), int(col)
        game.make_move(row, col)


class RandomPlayer:
    """Player that chooses a random move.
    """
    def __init__(self):
        self.mark = 'O'

    def get_move(self, game):
        """Choose a random move.
        """
        moves = game.get_possible_moves()
        return random.choice(moves)

    def move(self, game):
        """Make a move on the board.
        """
        move = self.get_move(game)
        game.make_move(*move)


def main():
    """Run the game.
    """
    player1 = HumanPlayer()
    player2 = RandomPlayer()
    game = Isolation(player1, player2)
    game.play()


if __name__ == '__main__':
    main()
