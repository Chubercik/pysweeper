import ctypes
import os

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = '1'

# as of right now, this will only
# work with a board of size 20x20
# and offsets of 100 pixels
position = (screensize[0] // 2 - 420,
            screensize[1] // 2 - 420)

os.environ["SDL_VIDEO_WINDOW_POS"] = f"{str(position[0])}, {str(position[1])}"

import pygame  # noqa: E402

screen = pygame.display.set_mode(flags=pygame.HIDDEN)

bomb_explode_sprite = pygame.image.load("textures/bomb_explode.png")
bomb_no_sprite = pygame.image.load("textures/bomb_no.png")
bomb_sprite = pygame.image.load("textures/bomb.png")

clock_null_sprite = pygame.image.load("textures/clock_null.png")
clock_zero_sprite = pygame.image.load("textures/clock_zero.png")
clock_one_sprite = pygame.image.load("textures/clock_one.png")
clock_two_sprite = pygame.image.load("textures/clock_two.png")
clock_three_sprite = pygame.image.load("textures/clock_three.png")
clock_four_sprite = pygame.image.load("textures/clock_four.png")
clock_five_sprite = pygame.image.load("textures/clock_five.png")
clock_six_sprite = pygame.image.load("textures/clock_six.png")
clock_seven_sprite = pygame.image.load("textures/clock_seven.png")
clock_eight_sprite = pygame.image.load("textures/clock_eight.png")
clock_nine_sprite = pygame.image.load("textures/clock_nine.png")

one_sprite = pygame.image.load("textures/one.png")
two_sprite = pygame.image.load("textures/two.png")
three_sprite = pygame.image.load("textures/three.png")
four_sprite = pygame.image.load("textures/four.png")
five_sprite = pygame.image.load("textures/five.png")
six_sprite = pygame.image.load("textures/six.png")
seven_sprite = pygame.image.load("textures/seven.png")
eight_sprite = pygame.image.load("textures/eight.png")

flag_sprite = pygame.image.load("textures/flag.png")

question_mark_sprite = pygame.image.load("textures/question_mark.png")

smiley_rip_sprite = pygame.image.load("textures/smiley_rip.png")
smiley_wow_sprite = pygame.image.load("textures/smiley_wow.png")
smiley_yeah_sprite = pygame.image.load("textures/smiley_yeah.png")
smiley_sprite = pygame.image.load("textures/smiley.png")


class Sprites:
    def __init__(self):
        self.sprites = {
            "bomb_explode": bomb_explode_sprite,
            "bomb_no": bomb_no_sprite,
            "bomb": bomb_sprite,
            "clock_null": clock_null_sprite,
            "clock_zero": clock_zero_sprite,
            "clock_one": clock_one_sprite,
            "clock_two": clock_two_sprite,
            "clock_three": clock_three_sprite,
            "clock_four": clock_four_sprite,
            "clock_five": clock_five_sprite,
            "clock_six": clock_six_sprite,
            "clock_seven": clock_seven_sprite,
            "clock_eight": clock_eight_sprite,
            "clock_nine": clock_nine_sprite,
            "one": one_sprite,
            "two": two_sprite,
            "three": three_sprite,
            "four": four_sprite,
            "five": five_sprite,
            "six": six_sprite,
            "seven": seven_sprite,
            "eight": eight_sprite,
            "flag": flag_sprite,
            "question_mark": question_mark_sprite,
            "smiley_rip": smiley_rip_sprite,
            "smiley_wow": smiley_wow_sprite,
            "smiley_yeah": smiley_yeah_sprite,
            "smiley": smiley_sprite
        }

        for i, sprite in self.sprites.items():
            sprite = sprite.convert_alpha()


def main():
    pass


if __name__ == "__main__":
    main()
