import itertools
import random
import tkinter
import tkinter.filedialog
from typing import List, Optional, Tuple

from PIL import Image

from sprites import Sprites, blit_sprite, game_offset, pg, screen

sprites = Sprites().sprites


digit_to_str = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine"
}


class Block:
    def __init__(self) -> None:
        self.is_bomb = False
        self.is_exploded = False
        self.is_flagged = False
        self.is_question_mark = False
        self.is_revealed = False
        self.number = 0
        self.x = 0
        self.y = 0

    def draw(self) -> None:
        wall = pg.surface.Surface((32, 32))
        wall.fill((30, 30, 30))
        screen.blit(wall, (self.x, self.y))
        wall = pg.transform.scale(wall, (30, 30))
        wall.fill((170, 170, 170))
        screen.blit(wall, (self.x + 1, self.y + 1))
        if self.is_revealed:
            wall.fill((85, 85, 85))
            screen.blit(wall, (self.x + 1, self.y + 1))
            if self.is_exploded:
                screen.blit(sprites["bomb_explode"], self.get_position())
            elif self.is_bomb:
                if self.is_flagged:
                    screen.blit(sprites["flag"], self.get_position())
                else:
                    screen.blit(sprites["bomb"], self.get_position())
            elif self.is_flagged:
                screen.blit(sprites["bomb_no"], self.get_position())
            elif self.number is not None and self.number != 0:
                blit_sprite(sprites[digit_to_str[self.number]],
                            (30, 30, 30),
                            self.get_position(),
                            screen)
        elif self.is_flagged:
            screen.blit(sprites["flag"], self.get_position())
        elif self.is_question_mark:
            screen.blit(sprites["question_mark"], self.get_position())
        else:
            screen.blit(sprites["tile"], self.get_position())

    def increase_number(self) -> None:
        self.number += 1

    def set_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def get_position(self) -> Tuple[int, int]:
        return (self.x, self.y)


class Board:
    def __init__(self, width: int, height: int, bomb_count: int) -> None:
        self.board: List[List[Block]] = []
        self.empty_tiles: List[Tuple[int, int]] = []
        self.width = width
        self.height = height
        self.bomb_count = bomb_count
        self.left_offset: int = game_offset
        self.top_offset: int = game_offset
        for i, y in enumerate(range(self.top_offset,
                                    self.top_offset + self.height*32,
                                    32)):
            self.board.append([])
            for j, x in enumerate(range(self.left_offset,
                                        self.left_offset + self.width*32,
                                        32)):
                self.board[i].append(Block())
                self.board[i][j].set_position(x, y)

        for y in range(self.height):
            self.empty_tiles.extend((x, y) for x in range(self.width))

        self.generate_bombs()
        self.generate_numbers()

        self.game_over: Optional[str] = None

    def generate_bombs(self) -> None:
        bomb_count = self.bomb_count
        if bomb_count > self.width * self.height:
            self.bomb_count = self.width * self.height - 1
            bomb_count = self.bomb_count
        while bomb_count > 0:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if not self.board[y][x].is_bomb:
                self.board[y][x].is_bomb = True
                self.empty_tiles.remove((x, y))
                bomb_count -= 1

    def generate_numbers(self) -> None:
        for y, x in itertools.product(range(self.height), range(self.width)):
            if not self.board[y][x].is_bomb:
                self.board[y][x].number = self.count_bombs(x, y)

    def count_bombs(self, x: int, y: int) -> int:
        return sum(bool((
                    0 <= x + i < self.width
                    and 0 <= y + j < self.height
                    and self.board[y + j][x + i].is_bomb
                )) for i, j in itertools.product(range(-1, 2), range(-1, 2)))

    def move_bomb(self, x: int, y: int) -> None:
        self.board[y][x].is_bomb = False
        for i, j in itertools.product(range(-1, 2), range(-1, 2)):
            if (
                0 <= x + i < self.width
                and 0 <= y + j < self.height
                and self.board[y + j][x + i].is_bomb
            ):
                self.board[y + j][x + i].number -= 1
                if self.board[y + j][x + i].is_bomb:
                    self.board[y][x].number += 1
        i = random.randint(0, len(self.empty_tiles) - 1)
        x = self.empty_tiles[i][0]
        y = self.empty_tiles[i][1]
        self.board[y][x].is_bomb = True
        for i, j in itertools.product(range(-1, 2), range(-1, 2)):
            if (
                0 <= x + i < self.width
                and 0 <= y + j < self.height
            ):
                self.board[y + j][x + i].number += 1

    def draw(self) -> None:
        for y, x in itertools.product(range(self.height), range(self.width)):
            self.board[y][x].draw()

    def reveal(self, x: int, y: int) -> None:
        if self.board[y][x].is_bomb:
            self.board[y][x].is_exploded = True
            for x, y in itertools.product(range(self.width),
                                          range(self.height)):
                self.board[y][x].is_revealed = True
            self.game_over = "LOSE"
        self.board[y][x].is_revealed = True
        if self.board[y][x].number == 0:
            for i, j in itertools.product(range(-1, 2), range(-1, 2)):
                if (
                    0 <= x + i < self.width
                    and 0 <= y + j < self.height
                    and not self.board[y + j][x + i].is_revealed
                    and not self.board[y + j][x + i].is_flagged
                ):
                    self.reveal(x + i, y + j)

    def check_win(self) -> bool:
        for y, x in itertools.product(range(self.height), range(self.width)):
            if not self.board[y][x].is_revealed \
               and not self.board[y][x].is_bomb:
                return False
        if self.game_over is None:
            self.game_over = "WIN"
            for x, y in itertools.product(range(self.width),
                                          range(self.height)):
                self.board[y][x].is_revealed = True
            return True
        return False

    def window_resize(self) -> None:
        for (i, y), (j, x) in itertools.product(
            enumerate(range(self.top_offset,
                            self.top_offset + self.height*32,
                            32)),
            enumerate(range(self.left_offset,
                            self.left_offset + self.width*32,
                            32))):
            self.board[i][j].set_position(x, y)


class Smiley:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.is_in_awe = False
        self.is_dead = False
        self.is_cool = False
        self.sprite: Optional[pg.surface.Surface] = None

    def draw(self, screen: pg.surface.Surface) -> None:
        screen.blit(pg.transform.scale(sprites["tile"], (64, 64)),
                    self.get_position())
        if self.is_in_awe:
            self.sprite = sprites["smiley_wow"]
        elif self.is_dead:
            self.sprite = sprites["smiley_rip"]
        elif self.is_cool:
            self.sprite = sprites["smiley_yeah"]
        else:
            self.sprite = sprites["smiley"]
        if self.sprite:
            self.sprite = pg.transform.scale(self.sprite, (64, 64))
            screen.blit(self.sprite, (self.x, self.y))

    def set_reset(self) -> None:
        self.is_dead = False
        self.is_in_awe = False
        self.is_cool = False

    def set_in_awe(self) -> None:
        self.is_in_awe = True
        self.is_dead = False
        self.is_cool = False

    def set_dead(self) -> None:
        self.is_in_awe = False
        self.is_dead = True
        self.is_cool = False

    def set_cool(self) -> None:
        self.is_in_awe = False
        self.is_dead = False
        self.is_cool = True

    def set_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def get_position(self) -> Tuple[int, int]:
        return (self.x, self.y)


class Timer:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.number = 0
        self.sprite: Optional[pg.surface.Surface] = None

    def draw(self, screen: pg.surface.Surface) -> None:
        wall = pg.surface.Surface((32, 64))
        wall.fill((30, 30, 30))
        screen.blit(wall, (self.x, self.y))
        wall = pg.transform.scale(wall, (30, 62))
        wall.fill((170, 170, 170))
        screen.blit(wall, (self.x + 1, self.y + 1))
        if self.number is not None:
            self.sprite = sprites[f"clock_{digit_to_str[self.number]}"]
        if self.sprite:
            self.sprite = pg.transform.scale(self.sprite, (32, 64))
            screen.blit(self.sprite, (self.x, self.y))

    def set_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def get_position(self) -> Tuple[int, int]:
        return (self.x, self.y)


def prompt_file() -> str:
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name


def png_to_ico(inp: str = "textures/icon.png", out: str = "icon.ico") -> None:
    img = Image.open(inp)
    icon_sizes = [(16, 16), (24, 24), (32, 32),
                  (48, 48), (64, 64), (128, 128),
                  (255, 255)]
    img.save(out, sizes=icon_sizes)


def main():
    pass


if __name__ == "__main__":
    main()
