from sys import exit

from utilities import Board, Smiley, Timer, pygame, screen


class Pysweeper:
    def __init__(self, width: int, height: int, bombs: int) -> None:
        self._width = width
        self._height = height
        self._bombs = bombs
        self._clicks = 0
        self._flags = 0
        self._question_marks = 0
        self._board = Board(width, height, bombs)
        self._smiley = Smiley(x=(self._board._left_offset - 32
                                 + 32*self._width//2),
                              y=(self._board._top_offset - 64))
        self._time = 0
        self._timer_0 = Timer(x=(self._board._left_offset + 32
                                 + 32*self._width//2),
                              y=(self._board._top_offset - 64))
        self._timer_1 = Timer(x=(self._board._left_offset + 64
                                 + 32*self._width//2),
                              y=(self._board._top_offset - 64))
        self._timer_2 = Timer(x=(self._board._left_offset + 96
                                 + 32*self._width//2),
                              y=(self._board._top_offset - 64))
        self._timer = [self._timer_0, self._timer_1, self._timer_2]
        self._score_0 = Timer(x=(self._board._left_offset - 128
                                 + 32*self._width//2),
                              y=(self._board._top_offset - 64))
        self._score_1 = Timer(x=(self._board._left_offset - 96
                                 + 32*self._width//2),
                              y=(self._board._top_offset - 64))
        self._score_2 = Timer(x=(self._board._left_offset - 64
                                 + 32*self._width//2),
                              y=(self._board._top_offset - 64))
        self._score = [self._score_0, self._score_1, self._score_2]
        self._score[0].set_number(self._bombs // 100)
        self._score[1].set_number(self._bombs // 10)
        self._score[2].set_number(self._bombs % 10)

    def run(self) -> None:
        pygame.init()
        pygame.mixer.init()

        play_sound = True

        pygame.display.set_caption("pysweeper")
        pygame.display.set_icon(pygame.image.load("textures/bomb.png"))
        pygame.display.set_mode(size=(32*self._width + 200,
                                      32*self._height + 200),
                                flags=pygame.RESIZABLE,
                                vsync=True)

        clock = pygame.time.Clock()

        while True:
            screen.fill((170, 170, 170))

            self._board.draw()
            self._smiley.draw(screen)
            for timer in self._timer:
                timer.draw(screen)
            for score in self._score:
                score.draw(screen)

            mouse_pos = pygame.mouse.get_pos()
            mouse_x = (mouse_pos[0] - self._board._left_offset) // 32
            mouse_y = (mouse_pos[1] - self._board._top_offset) // 32

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._smiley.set_in_awe()
                if event.type == pygame.MOUSEBUTTONUP:
                    self._smiley.set_reset()
                    if mouse_x < self._width and \
                       mouse_x >= 0 and \
                       mouse_y < self._height and \
                       mouse_y >= 0 and \
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
                            self._score[0].set_number((self._bombs - self._flags) // 100)
                            self._score[1].set_number((self._bombs - self._flags) // 10)
                            self._score[2].set_number((self._bombs - self._flags) % 10)

                        elif event.button == 2:
                            if block.is_question_mark():
                                self._question_marks -= 1
                                block.unquestion_mark()
                            else:
                                self._question_marks += 1
                                block.question_mark()
                    if mouse_pos[0] < self._smiley.get_position()[0] + 64 and \
                       mouse_pos[0] >= self._smiley.get_position()[0] and \
                       mouse_pos[1] < self._smiley.get_position()[1] + 64 and \
                       mouse_pos[1] >= self._smiley.get_position()[1]:
                        if event.button == 1:
                            self.__init__(self._width,
                                          self._height,
                                          self._bombs)
                            play_sound = True

            self._board.check_win()

            if self._board._game_over == "WIN":
                self._smiley.set_cool()

            if self._board._game_over == "LOSE":
                if play_sound:
                    pygame.mixer.music.load("sounds/explosion.mp3")
                    pygame.mixer.music.play()
                    play_sound = False
                self._smiley.set_dead()

            if self._board._game_over is None:
                self._time += 1/60
                self._timer[0].set_number(int(self._time) // 100)
                self._timer[1].set_number(int(self._time) // 10)
                self._timer[2].set_number(int(self._time) % 10)

            pygame.display.update()
            clock.tick(60)


def main():
    pass


if __name__ == "__main__":
    main()
