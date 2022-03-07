from sys import exit

from utilities import Board, Button, pygame, screen


class Pysweeper:
    def __init__(self, width: int, height: int, bombs: int) -> None:
        self._width = width
        self._height = height
        self._bombs = bombs
        self._clicks = 0
        self._flags = 0
        self._question_marks = 0
        self._board = Board(width, height, bombs)

    def run(self) -> None:
        pygame.init()
        pygame.display.set_caption("pysweeper")
        pygame.display.set_icon(pygame.image.load("textures/bomb.png"))
        clock = pygame.time.Clock()
        pygame.display.set_mode(size=(32*self._width + 160,
                                      32*self._height + 32),
                                flags=pygame.RESIZABLE,
                                vsync=True)

        while True:
            screen.fill((255, 255, 255))

            self._board.draw()

            mouse_pos = pygame.mouse.get_pos()
            mouse_x = mouse_pos[0] // 32
            mouse_y = mouse_pos[1] // 32

            text_font = pygame.font.Font("fonts/minecraft_regular.ttf", 16)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_x < self._width and \
                       mouse_y < self._height and \
                       self._board._game_over is None:
                        block = self._board._board[mouse_y][mouse_x]
                        if event.button == 1 and not block.is_revealed():
                            self._clicks += 1
                            self._board.reveal(mouse_x, mouse_y)
                        elif event.button == 3 and not block.is_revealed():
                            if block.is_flagged():
                                self._flags -= 1
                                block.unflag()
                            else:
                                self._flags += 1
                                block.flag()
                        elif event.button == 2:
                            if block.is_question_mark():
                                self._question_marks -= 1
                                block.unquestion_mark()
                            else:
                                self._question_marks += 1
                                block.question_mark()

            fps_counter = text_font.render(f"FPS: {int(clock.get_fps())}",
                                           True,
                                           (0, 0, 0))
            screen.blit(fps_counter, (32*self._width + 8, 8))

            num_flags = text_font.render(f"Bombs: {self._bombs - self._flags}",
                                         True,
                                         (0, 0, 0))
            screen.blit(num_flags, (32*self._width + 8, 40))

            num_clicks = text_font.render(f"Clicks: {self._clicks}",
                                          True,
                                          (0, 0, 0))
            screen.blit(num_clicks, (32*self._width + 8, 72))

            if self._board._game_over == "LOSE":
                dim_light = pygame.Surface((32*self._width, 32*self._height))
                dim_light.set_alpha(100)
                dim_light.fill((0, 0, 0))
                screen.blit(dim_light, (0, 0))
                button = Button(x=(32*self._width - 128)/2,
                                y=(32*self._height - 64)/2,
                                width=128,
                                height=64,
                                text="Restart")
                button.draw()
                if button.is_clicked(mouse_pos):
                    self.__init__(self._width, self._height, self._bombs)

            pygame.display.update()
            clock.tick(60)


def main():
    pass


if __name__ == "__main__":
    main()
