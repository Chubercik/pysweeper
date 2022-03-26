import itertools
import random
from typing import List, Optional, Tuple

from sprites import Sprites, blit_sprite, game_offset, pygame, screen

sprites = Sprites().sprites


class Block:
    def __init__(self) -> None:
        self._is_bomb = False
        self._is_exploded = False
        self._is_flagged = False
        self._is_question_mark = False
        self._is_revealed = False
        self._number = 0
        self._x = 0
        self._y = 0

    def draw(self) -> None:
        wall = pygame.surface.Surface((32, 32))
        wall.fill((30, 30, 30))
        screen.blit(wall, (self._x, self._y))
        wall = pygame.transform.scale(wall, (30, 30))
        wall.fill((170, 170, 170))
        screen.blit(wall, (self._x + 1, self._y + 1))
        if self.is_revealed():
            wall.fill((85, 85, 85))
            screen.blit(wall, (self._x + 1, self._y + 1))
            if self.is_exploded():
                screen.blit(sprites["bomb_explode"], self.get_position())
            elif self.is_bomb():
                if self.is_flagged():
                    screen.blit(sprites["flag"], self.get_position())
                else:
                    screen.blit(sprites["bomb"], self.get_position())
            elif self.is_flagged():
                screen.blit(sprites["bomb_no"], self.get_position())
            elif self.get_number() == 1:
                blit_sprite(sprites["one"],
                            (30, 30, 30),
                            self.get_position(),
                            screen)
            elif self.get_number() == 2:
                blit_sprite(sprites["two"],
                            (30, 30, 30),
                            self.get_position(),
                            screen)
            elif self.get_number() == 3:
                blit_sprite(sprites["three"],
                            (30, 30, 30),
                            self.get_position(),
                            screen)
            elif self.get_number() == 4:
                blit_sprite(sprites["four"],
                            (30, 30, 30),
                            self.get_position(),
                            screen)
            elif self.get_number() == 5:
                blit_sprite(sprites["five"],
                            (30, 30, 30),
                            self.get_position(),
                            screen)
            elif self.get_number() == 6:
                blit_sprite(sprites["six"],
                            (30, 30, 30),
                            self.get_position(),
                            screen)
            elif self.get_number() == 7:
                blit_sprite(sprites["seven"],
                            (30, 30, 30),
                            self.get_position(),
                            screen)
            elif self.get_number() == 8:
                blit_sprite(sprites["eight"],
                            (30, 30, 30),
                            self.get_position(),
                            screen)
        elif self.is_flagged():
            screen.blit(sprites["flag"], self.get_position())
        elif self.is_question_mark():
            screen.blit(sprites["question_mark"], self.get_position())
        else:
            screen.blit(sprites["tile"], self.get_position())

    def reveal(self) -> None:
        self._is_revealed = True

    def flag(self) -> None:
        self._is_flagged = True

    def question_mark(self) -> None:
        self._is_question_mark = True

    def unflag(self) -> None:
        self._is_flagged = False

    def unquestion_mark(self) -> None:
        self._is_question_mark = False

    def set_number(self, number: int) -> None:
        self._number = number

    def increase_number(self) -> None:
        self._number += 1

    def set_bomb(self) -> None:
        self._is_bomb = True

    def set_exploded(self) -> None:
        self._is_exploded = True

    def set_position(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def is_bomb(self) -> bool:
        return self._is_bomb

    def is_exploded(self) -> bool:
        return self._is_exploded

    def is_flagged(self) -> bool:
        return self._is_flagged

    def is_question_mark(self) -> bool:
        return self._is_question_mark

    def is_revealed(self) -> bool:
        return self._is_revealed

    def get_number(self) -> int:
        return self._number

    def get_position(self) -> Tuple[int, int]:
        return (self._x, self._y)


class Board:
    def __init__(self, width: int, height: int, bomb_count: int) -> None:
        self._board: List[List[Block]] = []
        self._empty_tiles: List[Tuple[int, int]] = []
        self._width = width
        self._height = height
        self._bomb_count = bomb_count
        self._left_offset: int = game_offset
        self._top_offset: int = game_offset
        for i, y in enumerate(range(self._left_offset,
                                    self._left_offset + self._height*32,
                                    32)):
            self._board.append([])
            for j, x in enumerate(range(self._top_offset,
                                        self._top_offset + self._width*32,
                                        32)):
                self._board[i].append(Block())
                self._board[i][j].set_position(x, y)

        for y in range(self._height):
            self._empty_tiles.extend((x, y) for x in range(self._width))

        self.generate_bombs()
        self.generate_numbers()

        self._game_over: Optional[str] = None

    def generate_bombs(self) -> None:
        bomb_count = self._bomb_count
        if bomb_count > self._width * self._height:
            self._bomb_count = self._width * self._height - 1
            bomb_count = self._bomb_count
        while bomb_count > 0:
            x = random.randint(0, self._width - 1)
            y = random.randint(0, self._height - 1)
            if not self._board[y][x].is_bomb():
                self._board[y][x].set_bomb()
                self._empty_tiles.remove((x, y))
                bomb_count -= 1

    def generate_numbers(self) -> None:
        for y, x in itertools.product(range(self._height), range(self._width)):
            if not self._board[y][x].is_bomb():
                self._board[y][x].set_number(self.count_bombs(x, y))

    def count_bombs(self, x: int, y: int) -> int:
        return sum(bool((
                    0 <= x + i < self._width
                    and 0 <= y + j < self._height
                    and self._board[y + j][x + i].is_bomb()
                )) for i, j in itertools.product(range(-1, 2), range(-1, 2)))

    def move_bomb(self, x: int, y: int) -> None:
        self._board[y][x]._is_bomb = False
        for i, j in itertools.product(range(-1, 2), range(-1, 2)):
            if (
                0 <= x + i < self._width
                and 0 <= y + j < self._height
                and self._board[y + j][x + i].is_bomb()
            ):
                self._board[y + j][x + i]._number -= 1
                if self._board[y + j][x + i].is_bomb():
                    self._board[y][x]._number += 1
        i = random.randint(0, len(self._empty_tiles) - 1)
        x = self._empty_tiles[i][0]
        y = self._empty_tiles[i][1]
        self._board[y][x].set_bomb()
        for i, j in itertools.product(range(-1, 2), range(-1, 2)):
            if (
                0 <= x + i < self._width
                and 0 <= y + j < self._height
            ):
                self._board[y + j][x + i]._number += 1

    def draw(self) -> None:
        for y, x in itertools.product(range(self._height), range(self._width)):
            self._board[y][x].draw()

    def reveal(self, x: int, y: int) -> None:
        if self._board[y][x].is_bomb():
            self._board[y][x].set_exploded()
            for x, y in itertools.product(range(self._width), range(self._height)):
                self._board[y][x].reveal()
            self._game_over = "LOSE"
        self._board[y][x].reveal()
        if self._board[y][x].get_number() == 0:
            for i, j in itertools.product(range(-1, 2), range(-1, 2)):
                if (
                    0 <= x + i < self._width
                    and 0 <= y + j < self._height
                    and not self._board[y + j][x + i].is_revealed()
                    and not self._board[y + j][x + i].is_flagged()
                ):
                    self.reveal(x + i, y + j)

    def check_win(self) -> bool:
        for y, x in itertools.product(range(self._height), range(self._width)):
            if not self._board[y][x].is_revealed() \
               and not self._board[y][x].is_bomb():
                return False
        if self._game_over is None:
            self._game_over = "WIN"
            for x, y in itertools.product(range(self._width), range(self._height)):
                self._board[y][x].reveal()
            return True
        return False


class Smiley:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y
        self._is_in_awe = False
        self._is_dead = False
        self._is_cool = False
        self._sprite: Optional[pygame.surface.Surface] = None

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(pygame.transform.scale(sprites["tile"], (64, 64)),
                    self.get_position())
        if self._is_in_awe:
            self._sprite = sprites["smiley_wow"]
        elif self._is_dead:
            self._sprite = sprites["smiley_rip"]
        elif self._is_cool:
            self._sprite = sprites["smiley_yeah"]
        else:
            self._sprite = sprites["smiley"]
        if self._sprite:
            self._sprite = pygame.transform.scale(self._sprite, (64, 64))
            screen.blit(self._sprite, (self._x, self._y))

    def set_reset(self) -> None:
        self._is_dead = False
        self._is_in_awe = False
        self._is_cool = False

    def set_in_awe(self) -> None:
        self._is_in_awe = True
        self._is_dead = False
        self._is_cool = False

    def set_dead(self) -> None:
        self._is_in_awe = False
        self._is_dead = True
        self._is_cool = False

    def set_cool(self) -> None:
        self._is_in_awe = False
        self._is_dead = False
        self._is_cool = True

    def is_in_awe(self) -> bool:
        return self._is_in_awe

    def is_dead(self) -> bool:
        return self._is_dead

    def is_cool(self) -> bool:
        return self._is_cool

    def set_position(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def get_position(self) -> Tuple[int, int]:
        return (self._x, self._y)


class Timer:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y
        self._number = 0
        self._sprite: Optional[pygame.surface.Surface] = None

    def draw(self, screen: pygame.surface.Surface) -> None:
        wall = pygame.surface.Surface((32, 64))
        wall.fill((30, 30, 30))
        screen.blit(wall, (self._x, self._y))
        wall = pygame.transform.scale(wall, (30, 62))
        wall.fill((170, 170, 170))
        screen.blit(wall, (self._x + 1, self._y + 1))
        if self._number == 0:
            self._sprite = sprites["clock_zero"]
        elif self._number == 1:
            self._sprite = sprites["clock_one"]
        elif self._number == 2:
            self._sprite = sprites["clock_two"]
        elif self._number == 3:
            self._sprite = sprites["clock_three"]
        elif self._number == 4:
            self._sprite = sprites["clock_four"]
        elif self._number == 5:
            self._sprite = sprites["clock_five"]
        elif self._number == 6:
            self._sprite = sprites["clock_six"]
        elif self._number == 7:
            self._sprite = sprites["clock_seven"]
        elif self._number == 8:
            self._sprite = sprites["clock_eight"]
        elif self._number == 9:
            self._sprite = sprites["clock_nine"]
        if self._sprite:
            self._sprite = pygame.transform.scale(self._sprite, (32, 64))
            screen.blit(self._sprite, (self._x, self._y))

    def set_number(self, number: int) -> None:
        self._number = number

    def get_number(self) -> int:
        return self._number

    def set_position(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def get_position(self) -> Tuple[int, int]:
        return (self._x, self._y)


def main():
    pass


if __name__ == "__main__":
    main()
