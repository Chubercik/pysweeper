import os
from typing import Tuple

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = '1'

from sys import exit  # noqa: E402

import pygame  # noqa: E402

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("pysweeper")
pygame.display.set_icon(pygame.image.load("textures/bomb.png"))
clock = pygame.time.Clock()

smiley_sprite = pygame.image.load("textures/smiley.png")
bomb_sprite = pygame.image.load("textures/bomb.png")
flag_sprite = pygame.image.load("textures/flag.png")
question_mark_sprite = pygame.image.load("textures/question_mark.png")

one_sprite = pygame.image.load("textures/one.png")
two_sprite = pygame.image.load("textures/two.png")
three_sprite = pygame.image.load("textures/three.png")
four_sprite = pygame.image.load("textures/four.png")
five_sprite = pygame.image.load("textures/five.png")
six_sprite = pygame.image.load("textures/six.png")
seven_sprite = pygame.image.load("textures/seven.png")
eight_sprite = pygame.image.load("textures/eight.png")


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
        if self.is_revealed:
            if self.is_bomb:
                screen.blit(bomb_sprite, (self.x, self.y))
            elif self.number == 1:
                screen.blit(one_sprite, (self.x, self.y))
            elif self.number == 2:
                screen.blit(two_sprite, (self.x, self.y))
            elif self.number == 3:
                screen.blit(three_sprite, (self.x, self.y))
            elif self.number == 4:
                screen.blit(four_sprite, (self.x, self.y))
            elif self.number == 5:
                screen.blit(five_sprite, (self.x, self.y))
            elif self.number == 6:
                screen.blit(six_sprite, (self.x, self.y))
            elif self.number == 7:
                screen.blit(seven_sprite, (self.x, self.y))
            elif self.number == 8:
                screen.blit(eight_sprite, (self.x, self.y))
        elif self.is_flagged:
            screen.blit(flag_sprite, (self.x, self.y))
        elif self.is_question_mark:
            screen.blit(question_mark_sprite, (self.x, self.y))
        else:
            wall = pygame.transform.scale(smiley_sprite, (32, 32))
            wall.fill("gray")
            screen.blit(wall, (self.x, self.y))

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
        return self.x, self.y


x = 0
y = 0
x_switch = 1
y_switch = 1

scale = 2

test_font = pygame.font.Font("fonts/minecraft_regular.ttf", 20)
text_surface = test_font.render("Welcome to pysweeper!", False, (0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((255, 255, 255))

    smiley_scaled = pygame.transform.scale(smiley_sprite,
                                           (smiley_sprite.get_width()*scale,
                                            smiley_sprite.get_height()*scale))

    if x > 800 - smiley_sprite.get_width()*scale:
        x_switch = -1
    if x < 0:
        x_switch = 1
    if y > 400 - smiley_sprite.get_height()*scale:
        y_switch = -1
    if y < 0:
        y_switch = 1
    x += x_switch
    y += y_switch

    screen.blit(text_surface, (10, 10))
    screen.blit(one_sprite, (0, 100))
    screen.blit(two_sprite, (32, 100))
    screen.blit(three_sprite, (64, 100))
    screen.blit(four_sprite, (96, 100))
    screen.blit(five_sprite, (128, 100))
    screen.blit(six_sprite, (160, 100))
    screen.blit(seven_sprite, (192, 100))
    screen.blit(eight_sprite, (224, 100))
    screen.blit(bomb_sprite, (256, 100))
    screen.blit(flag_sprite, (288, 100))
    screen.blit(question_mark_sprite, (320, 100))
    screen.blit(smiley_scaled, (x, y))
    block = Block()
    for i in range(10):
        block.set_position(x + 64 + i*36, y)
        block.draw()
    pygame.display.update()
    clock.tick(144)
