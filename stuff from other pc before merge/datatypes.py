from __future__ import annotations

from dataclasses import dataclass, field
from random import randint
from typing import List, Optional


@dataclass
class Position:
    x: int
    y: int

    def neighbours(self, bounds: Optional[Rectangle] = None):
        """
        Yields all neighbouring positions which fit in the given rectangle.
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

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __iter__(self):
        return iter((self.x, self.y))


@dataclass(order=True)
class Point:
    value: int = field(default=0)
    bomb: bool = field(default=False)
    pos: Position = field(default=Position(0, 0))

    def __str__(self):
        return '{' + f"v: {self.value}, b: {self.bomb}" + '}'


@dataclass
class Rectangle:
    _bl: Position   # bottom left vertex
    _tr: Position   # top right vertex

    def __post_init__(self):
        if self._bl.x > self._tr.x:
            tmp = self._bl.x
            self._bl.x = self._tr.x
            self._tr.x = tmp
        if self._bl.y > self._tr.y:
            tmp = self._bl.y
            self._bl.y = self._tr.y
            self._tr.y = tmp

    def __contains__(self, position: Position) -> True:
        """
        Checks if a position fits inside the rectangle.
        """
        return position.x >= self._bl.x and position.y >= self._bl.y and \
            position.x <= self._tr.x and position.y <= self._tr.y


class Graph:
    """
    Class representing a 2D graph.
    """

    def __init__(self, height: int, width: int) -> None:
        """
        Initializes a Graph object.
        """

        self._height = height
        self._width = width
        self._bounds = Rectangle(
            Position(0, 0), Position(self._width-1, self._height-1))

        self._graph: List[List[Point]] = []
        for y in range(height):
            graph_line: List[Point] = []
            for x in range(self._width):
                graph_line.append(Point(0, False, Position(x, self._height - 1 - y)))
            self._graph.append(graph_line)

    def _get(self, position: Position) -> Point:
        """
        Returns a point given the position.
        """
        return self._graph[(self._height - position.y - 1)][(position.x)]

    def print_graph(self) -> str:
        graph_str = ""
        for line in self._graph:
            for point in line:
                graph_str += f"{str(point.value)} " if point.value != 0 else "  "
            graph_str = graph_str[:-1]
            graph_str += "\n"
        graph_str = graph_str[:-1]
        return graph_str

    def print_bombs(self) -> str:
        graph_str = ""
        for line in self._graph:
            for point in line:
                graph_str += "1 " if point.bomb else "0 "
            graph_str = graph_str[:-1]
            graph_str += "\n"
        graph_str = graph_str[:-1]
        return graph_str

    def print_pos(self) -> str:
        graph_str = ""
        for line in self._graph:
            for point in line:
                graph_str += f"{str(point.pos)} "
            graph_str = graph_str[:-1]
            graph_str += "\n"
        graph_str = graph_str[:-1]
        return graph_str

    def scatter_bombs(self) -> None:
        for line in self._graph:
            for point in line:
                rand_num = randint(0, 9)
                if rand_num == 7:
                    point.value = 'X'
                    point.bomb = True
                    for neighbour in point.pos.neighbours(self._bounds):
                        if str(self._get(neighbour).value).isdigit() is True:
                            self._get(neighbour).value += 1


class Color:
    def __init__(self, *rgb_colors):
        # Check if passing a tuple with three elements, like on draw_image
        self.r, self.g, self.b = rgb_colors[0] if len(rgb_colors) == 1 \
                                               else rgb_colors

    def __iter__(self):
        return iter((self.r, self.g, self.b))

    def copy(self):
        return Color(self.r, self.g, self.b)
