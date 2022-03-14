import random
from typing import Tuple

from sprites import Sprites, pygame, screen

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
        wall = pygame.Surface((32, 32))
        wall.fill((30, 30, 30))
        screen.blit(wall, (self._x, self._y))
        wall = pygame.transform.scale(wall, (30, 30))
        wall.fill((150, 150, 150))
        screen.blit(wall, (self._x + 1, self._y + 1))
        if self.is_revealed():
            wall.fill((100, 100, 100))
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
                screen.blit(sprites["one"], self.get_position())
            elif self.get_number() == 2:
                screen.blit(sprites["two"], self.get_position())
            elif self.get_number() == 3:
                screen.blit(sprites["three"], self.get_position())
            elif self.get_number() == 4:
                screen.blit(sprites["four"], self.get_position())
            elif self.get_number() == 5:
                screen.blit(sprites["five"], self.get_position())
            elif self.get_number() == 6:
                screen.blit(sprites["six"], self.get_position())
            elif self.get_number() == 7:
                screen.blit(sprites["seven"], self.get_position())
            elif self.get_number() == 8:
                screen.blit(sprites["eight"], self.get_position())
        elif self.is_flagged():
            screen.blit(sprites["flag"], self.get_position())
        elif self.is_question_mark():
            screen.blit(sprites["question_mark"], self.get_position())

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

    def get_position(self) -> Tuple[int]:
        return (self._x, self._y)


class Board:
    def __init__(self, width: int, height: int, bomb_count: int) -> None:
        self._board = []
        self._width = width
        self._height = height
        self._bomb_count = bomb_count
        self._left_offset = 100
        self._top_offset = 100
        for i, y in enumerate(range(self._left_offset,
                                    self._left_offset + self._height*32,
                                    32)):
            self._board.append([])
            for j, x in enumerate(range(self._top_offset,
                                        self._top_offset + self._width*32,
                                        32)):
                self._board[i].append(Block())
                self._board[i][j].set_position(x, y)

        self.generate_bombs()
        self.generate_numbers()

        self._game_over = None

    def generate_bombs(self) -> None:
        bomb_count = self._bomb_count
        if bomb_count > self._width * self._height:
            bomb_count = self._width * self._height
        while bomb_count > 0:
            x = random.randint(0, self._width - 1)
            y = random.randint(0, self._height - 1)
            if not self._board[y][x].is_bomb():
                self._board[y][x].set_bomb()
                bomb_count -= 1

    def generate_numbers(self) -> None:
        for y in range(self._height):
            for x in range(self._width):
                if not self._board[y][x].is_bomb():
                    self._board[y][x].set_number(self.count_bombs(x, y))

    def count_bombs(self, x: int, y: int) -> int:
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (
                    0 <= x + i < self._width
                    and 0 <= y + j < self._height
                    and self._board[y + j][x + i].is_bomb()
                ):
                    count += 1
        return count

    def draw(self) -> None:
        for y in range(self._height):
            for x in range(self._width):
                self._board[y][x].draw()

    def reveal(self, x: int, y: int) -> None:
        if self._board[y][x].is_bomb():
            self._board[y][x].set_exploded()
            for x in range(self._width):
                for y in range(self._height):
                    self._board[y][x].reveal()
            self._game_over = "LOSE"
        self._board[y][x].reveal()
        if self._board[y][x].get_number() == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (
                        0 <= x + i < self._width
                        and 0 <= y + j < self._height
                        and not self._board[y + j][x + i].is_revealed()
                    ):
                        self.reveal(x + i, y + j)


class Smiley:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y
        self._is_in_awe = False
        self._is_dead = False
        self._is_cool = False
        self._sprite = None

    def draw(self, screen: pygame.Surface) -> None:
        if self._is_in_awe:
            self._sprite = sprites["smiley_wow"]
        elif self._is_dead:
            self._sprite = sprites["smiley_rip"]
        elif self._is_cool:
            self._sprite = sprites["smiley_yeah"]
        else:
            self._sprite = sprites["smiley"]
        self._sprite = pygame.transform.scale(self._sprite, (64, 64))
        screen.blit(self._sprite, (self._x, self._y))

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

    def get_position(self) -> Tuple[int]:
        return (self._x, self._y)


class Button:
    def __init__(self, x: int, y: int,
                 width: int, height: int,
                 text: str) -> None:
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._text = text

    def draw(self) -> None:
        wall = pygame.Surface((self._width, self._height))
        wall.fill((30, 30, 30))
        screen.blit(wall, (self._x, self._y))
        wall = pygame.transform.scale(wall, (self._width - 10,
                                             self._height - 10))
        wall.fill((250, 250, 250))
        screen.blit(wall, (self._x + 5, self._y + 5))
        font = pygame.font.Font("fonts/minecraft_regular.ttf", 16)
        text = font.render(self._text, True, (0, 0, 0))
        screen.blit(text, (self._x + self._width / 2 - text.get_width() / 2,
                           self._y + self._height / 2 - text.get_height() / 2))

    def is_clicked(self, pos: Tuple[int]) -> bool:
        if pos[0] > self._x and pos[0] < self._x + self._width:
            if pos[1] > self._y and pos[1] < self._y + self._height:
                if pygame.mouse.get_pressed()[0]:
                    return True
        return False


def sec_to_time(sec: int) -> str:
    m = int(sec // 60)
    s = round(sec % 60, 2)
    if m < 10:
        m = f"0{m}"
    if s < 10:
        s = f"0{s}"
    return f"{m}:{s}"


def main():
    pass


if __name__ == "__main__":
    main()
