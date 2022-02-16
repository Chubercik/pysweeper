from __future__ import annotations

from dataclasses import dataclass, field
from random import randint
from typing import List, Optional


@dataclass
class Position:
    """
    Class representing a position in a 2D grid.

    Attributes:
        x: The x-coordinate of the position.
        y: The y-coordinate of the position.

    Methods:
        neighbours: Returns all (8) neighbouring positions
        which fit in the given rectangle.
    """
    x: int
    y: int

    def neighbours(self, bounds: Optional[Rectangle] = None) -> None:
        """
        Yields all (8) neighbouring positions which fit in the given rectangle.
        """
        d = [-1, 1]
        for dx in d:
            pos = Position(self.x + dx, self.y)
            if bounds is None or pos in bounds:
                yield pos
        for dy in d:
            pos = Position(self.x, self.y + dy)
            if bounds is None or pos in bounds:
                yield pos

        for dx in d:
            for dy in d:
                pos = Position(self.x + dx, self.y + dy)
                if bounds is None or pos in bounds:
                    yield pos

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


@dataclass
class Field:
    """
    Class representing a Minesweeper field.

    Attributes:
        value: The value of the field.
        bomb: Whether the field contains a bomb.
        pos: The position of the field.
    """
    value: int = field(default=0)
    bomb: bool = field(default=False)
    pos: Position = field(default=Position(0, 0))


@dataclass
class Rectangle:
    _bl: Position   # bottom left vertex
    _tr: Position   # top right vertex

    def __post_init__(self) -> None:
        if self._bl.x > self._tr.x:
            tmp = self._bl.x
            self._bl.x = self._tr.x
            self._tr.x = tmp
        if self._bl.y > self._tr.y:
            tmp = self._bl.y
            self._bl.y = self._tr.y
            self._tr.y = tmp

    def __contains__(self, position: Position) -> bool:
        """
        Checks if a position fits inside the rectangle.
        """
        return position.x >= self._bl.x and position.y >= self._bl.y and \
            position.x <= self._tr.x and position.y <= self._tr.y


class Board:
    """
    Class representing a game board.

    Attributes:
        height: The height of the board.
        width: The width of the board.
        board: The board itself.
        bounds: The bounds of the board.

    Methods:
        get_field: Returns a field given the position.
        scatter_bombs: Scatters bombs on the board.
        print_board: Prints the board.
        print_bombs: Prints the bombs.
        print_pos: Prints the positions.
    """

    def __init__(self, height: int, width: int) -> None:
        self._height = height
        self._width = width
        self._bounds = Rectangle(
            Position(0, 0), Position(self._width-1, self._height-1))

        self._board: List[List[Field]] = []
        for y in range(height):
            board_line: List[Field] = [
                Field(0, False, Position(x, self._height - 1 - y))
                for x in range(self._width)]

            self._board.append(board_line)

    def get_field(self, position: Position) -> Field:
        """
        Returns a field given the position.
        """
        return self._board[(self._height - position.y - 1)][(position.x)]

    def scatter_bombs(self) -> None:
        """
        Scatters bombs on the board.
        """
        for line in self._board:
            for point in line:
                rand_num = randint(0, 9)
                if rand_num == 7:
                    point.value = 'X'
                    point.bomb = True
                    for neighbour in point.pos.neighbours(self._bounds):
                        if str(self.get_field(neighbour).value).isdigit():
                            self.get_field(neighbour).value += 1

    def print_board(self) -> str:
        """
        Prints the board.
        """
        board_str = ''
        for line in self._board:
            for point in line:
                board_str += f"{point.value} "
            board_str = board_str[:-1]
            board_str += '\n'
        board_str = board_str[:-1]
        return board_str

    def print_bombs(self) -> str:
        """
        Prints the bombs.
        """
        board_str = ''
        for line in self._board:
            for point in line:
                board_str += "1 " if point.bomb else "0 "
            board_str = board_str[:-1]
            board_str += '\n'
        board_str = board_str[:-1]
        return board_str

    def print_pos(self) -> str:
        """
        Prints the positions.
        """
        board_str = ''
        for line in self._board:
            for point in line:
                board_str += f"{point.pos} "
            board_str = board_str[:-1]
            board_str += '\n'
        board_str = board_str[:-1]
        return board_str


def main():
    board = Board(10, 10)
    board.scatter_bombs()
    print(board.print_board())
    print()
    print(board.print_bombs())
    print()
    print(board.print_pos())


if __name__ == "__main__":
    main()
