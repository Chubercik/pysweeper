import random
from typing import Tuple

from sprites import pygame, screen, sprites


class Block:
    def __init__(self) -> None:
        self.is_bomb = False
        self.is_flagged = False
        self.is_question_mark = False
        self.is_revealed = False
        self.number = 0
        self.x = 0
        self.y = 0

    def draw(self) -> None:
        wall = pygame.Surface((32, 32))
        wall.fill((30, 30, 30))
        screen.blit(wall, (self.x, self.y))
        wall = pygame.transform.scale(wall, (30, 30))
        wall.fill((150, 150, 150))
        screen.blit(wall, (self.x + 1, self.y + 1))
        if self.is_revealed:
            if self.number in range(9):
                wall.fill((100, 100, 100))
                screen.blit(wall, (self.x + 1, self.y + 1))
            if self.is_bomb:
                screen.blit(sprites["bomb"], (self.x, self.y))
            elif self.number == 1:
                screen.blit(sprites["one"], (self.x, self.y))
            elif self.number == 2:
                screen.blit(sprites["two"], (self.x, self.y))
            elif self.number == 3:
                screen.blit(sprites["three"], (self.x, self.y))
            elif self.number == 4:
                screen.blit(sprites["four"], (self.x, self.y))
            elif self.number == 5:
                screen.blit(sprites["five"], (self.x, self.y))
            elif self.number == 6:
                screen.blit(sprites["six"], (self.x, self.y))
            elif self.number == 7:
                screen.blit(sprites["seven"], (self.x, self.y))
            elif self.number == 8:
                screen.blit(sprites["eight"], (self.x, self.y))
        elif self.is_flagged:
            screen.blit(sprites["flag"], (self.x, self.y))
        elif self.is_question_mark:
            screen.blit(sprites["question_mark"], (self.x, self.y))

    def reveal(self) -> None:
        self.is_revealed = True

    def flag(self) -> None:
        self.is_flagged = True

    def question_mark(self) -> None:
        self.is_question_mark = True

    def unflag(self) -> None:
        self.is_flagged = False

    def unquestion_mark(self) -> None:
        self.is_question_mark = False

    def set_number(self, number: int) -> None:
        self.number = number

    def increase_number(self) -> None:
        self.number += 1

    def set_bomb(self) -> None:
        self.is_bomb = True

    def set_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def is_bomb(self) -> bool:
        return self.is_bomb

    def is_flagged(self) -> bool:
        return self.is_flagged

    def is_question_mark(self) -> bool:
        return self.is_question_mark

    def is_revealed(self) -> bool:
        return self.is_revealed

    def get_number(self) -> int:
        return self.number

    def get_position(self) -> Tuple[int]:
        return (self.x, self.y)


class Board:
    def __init__(self, width: int, height: int, bomb_count: int) -> None:
        self.board = []
        self.width = width
        self.height = height
        self.bomb_count = bomb_count
        for i, y in enumerate(range(0, self.height*32, 32)):
            self.board.append([])
            for j, x in enumerate(range(0, self.width*32, 32)):
                self.board[i].append(Block())
                self.board[i][j].set_position(x, y)

        self.generate_bombs()
        self.generate_numbers()

    def generate_bombs(self) -> None:
        bomb_count = self.bomb_count
        while bomb_count > 0:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if not self.board[y][x].is_bomb:
                self.board[y][x].set_bomb()
                bomb_count -= 1

    def generate_numbers(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if not self.board[y][x].is_bomb:
                    self.board[y][x].set_number(self.count_bombs(x, y))

    def count_bombs(self, x: int, y: int) -> int:
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (
                    0 <= x + i < self.width
                    and 0 <= y + j < self.height
                    and self.board[y + j][x + i].is_bomb
                ):
                    count += 1
        return count

    def draw(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.board[y][x].draw()

    def reveal(self, x: int, y: int) -> None:
        self.board[y][x].reveal()
        if self.board[y][x].get_number() == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (
                        0 <= x + i < self.width
                        and 0 <= y + j < self.height
                        and not self.board[y + j][x + i].is_revealed
                    ):
                        self.reveal(x + i, y + j)
