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


sprites_folder_path = load_file("textures/")


def image_loader(path: str) -> str:
    for i in os.listdir(path):
        yield ((os.path.splitext(i)[0]),
               pygame.image.load(path + i).convert_alpha())


class Sprites:
    def __init__(self):
        self.sprites = dict(image_loader(sprites_folder_path))


def main():
    pass


if __name__ == "__main__":
    main()
