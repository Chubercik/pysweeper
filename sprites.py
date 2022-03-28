import os
from typing import Tuple

from screeninfo import get_monitors  # type: ignore

from file_io import read_json


def load_file(file_name: str) -> str:
    return os.path.join(os.path.dirname(__file__), file_name)


game_info = read_json(load_file("data/config.json"))
game_width = game_info["width"]*32
game_height = game_info["height"]*32
game_offset = game_info["offset"]


def get_screen_size() -> Tuple[int, int]:
    return next(((m.width, m.height) for m in get_monitors() if m.is_primary),
                (0, 0))


screensize = get_screen_size()

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = '1'

# as of right now, this will only
# work with a board of size 20x20
# and offsets of 100 pixels
position = (screensize[0] // 2 - game_width // 2 - game_offset,
            screensize[1] // 2 - game_height // 2 - game_offset)

os.environ["SDL_VIDEO_WINDOW_POS"] = f"{str(position[0])}, {str(position[1])}"

import pygame  # noqa: E402

screen = pygame.display.set_mode(flags=pygame.HIDDEN)


def img_outline(img: pygame.surface.Surface,
                color: Tuple[int, int, int],
                loc: Tuple[int, int],
                screen: pygame.surface.Surface) -> None:
    mask = pygame.mask.from_surface(img)
    mask_outline = mask.outline()
    mask_surf = pygame.Surface(img.get_size())
    for pixel in mask_outline:
        mask_surf.set_at(pixel, color)
    mask_surf.set_colorkey((0, 0, 0))
    screen.blit(mask_surf, (loc[0] - 1, loc[1]))
    screen.blit(mask_surf, (loc[0] + 1, loc[1]))
    screen.blit(mask_surf, (loc[0], loc[1] - 1))
    screen.blit(mask_surf, (loc[0], loc[1] + 1))


def blit_sprite(sprite: pygame.surface.Surface,
                outline_color: Tuple[int, int, int],
                location: Tuple[int, int],
                screen: pygame.surface.Surface) -> None:
    img_outline(sprite, outline_color, location, screen)
    screen.blit(sprite, location)


bomb_explode_sprite = pygame.image.load(load_file("textures/bomb_explode.png"))
bomb_no_sprite = pygame.image.load(load_file("textures/bomb_no.png"))
bomb_sprite = pygame.image.load(load_file("textures/bomb.png"))

clock_null_sprite = pygame.image.load(load_file("textures/clock_null.png"))
clock_zero_sprite = pygame.image.load(load_file("textures/clock_zero.png"))
clock_one_sprite = pygame.image.load(load_file("textures/clock_one.png"))
clock_two_sprite = pygame.image.load(load_file("textures/clock_two.png"))
clock_three_sprite = pygame.image.load(load_file("textures/clock_three.png"))
clock_four_sprite = pygame.image.load(load_file("textures/clock_four.png"))
clock_five_sprite = pygame.image.load(load_file("textures/clock_five.png"))
clock_six_sprite = pygame.image.load(load_file("textures/clock_six.png"))
clock_seven_sprite = pygame.image.load(load_file("textures/clock_seven.png"))
clock_eight_sprite = pygame.image.load(load_file("textures/clock_eight.png"))
clock_nine_sprite = pygame.image.load(load_file("textures/clock_nine.png"))

one_sprite = pygame.image.load(load_file("textures/one.png"))
two_sprite = pygame.image.load(load_file("textures/two.png"))
three_sprite = pygame.image.load(load_file("textures/three.png"))
four_sprite = pygame.image.load(load_file("textures/four.png"))
five_sprite = pygame.image.load(load_file("textures/five.png"))
six_sprite = pygame.image.load(load_file("textures/six.png"))
seven_sprite = pygame.image.load(load_file("textures/seven.png"))
eight_sprite = pygame.image.load(load_file("textures/eight.png"))

flag_sprite = pygame.image.load(load_file("textures/flag.png"))

question_mark_sprite = pygame.image.load(load_file("textures/question_mark.png"))

smiley_rip_sprite = pygame.image.load(load_file("textures/smiley_rip.png"))
smiley_wow_sprite = pygame.image.load(load_file("textures/smiley_wow.png"))
smiley_yeah_sprite = pygame.image.load(load_file("textures/smiley_yeah.png"))
smiley_sprite = pygame.image.load(load_file("textures/smiley.png"))

tile = pygame.image.load(load_file("textures/tile.png"))


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
            "smiley": smiley_sprite,
            "tile": tile
        }

        for i, sprite in self.sprites.items():
            sprite = sprite.convert_alpha()


def main():
    # Testing automatic loading of sprites
    sprites_folder_path = "textures/"

    def image_loader(path) -> str:
        for i in os.listdir(path):
            yield ((os.path.splitext(i)[0]),
                   pygame.image.load(path + i).convert_alpha)

    images = dict(image_loader(sprites_folder_path))

    for image in images:
        print(image, end='')

    print()

    sprites = Sprites().sprites

    for sprite in sprites:
        print(sprite, end='')


if __name__ == "__main__":
    main()
