import itertools
import platform
from sys import exit

from file_io import read_json, write_json
from sprites import load_file
from utilities import Board, Smiley, Timer, pygame, screen

if platform.system() == "Windows":
    sys_name = "Windows"
    import win32api  # type: ignore
    import win32gui  # type: ignore
    dc = win32gui.GetDC(0)
    white = win32api.RGB(255, 255, 255)
elif platform.system() == "Linux":
    sys_name = "Linux"
elif platform.system() == "Darwin":
    sys_name = "Mac"


class Pysweeper:
    def __init__(self,
                 width: int,
                 height: int,
                 bombs: int,
                 jr_reveal: bool = False) -> None:
        self._width = width
        self._height = height
        self._clicks = 0
        self._flags = 0
        self._question_marks = 0
        self._board = Board(width, height, bombs)
        self._bombs = self._board._bomb_count
        self._smiley = Smiley(x=(self._board._left_offset - 32
                                 + 32*self._width//2),
                              y=(self._board._top_offset - 64))
        self._time: float = 0
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
        self._score[1].set_number((self._bombs % 100) // 10)
        self._score[2].set_number(self._bombs % 10)
        self._first_move = True
        self._play_sound = True
        self._new_highscore = True
        self._jr_reveal = jr_reveal

    def run(self) -> None:
        pygame.init()
        pygame.mixer.init()

        pygame.display.set_caption("pysweeper")
        pygame.display.set_icon(pygame.image.load(load_file("textures/bomb.png")))
        pygame.display.set_mode(size=(32*self._width + 200,
                                      32*self._height + 200),
                                flags=pygame.RESIZABLE,
                                vsync=True)

        clock = pygame.time.Clock()

        if sys_name == "Windows":
            temp = win32gui.GetPixel(dc, 0, 0)
            input_arr = []
            cheat = False

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

            if cheat and sys_name == "Windows" and \
               mouse_x < self._width and mouse_x >= 0 and \
               mouse_y < self._height and mouse_y >= 0 and \
               not self._board._board[mouse_y][mouse_x].is_bomb():
                win32gui.SetPixel(dc, 0, 0, white)
            elif sys_name == "Windows":
                win32gui.SetPixel(dc, 0, 0, temp)

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
                        if event.button == 1 and not block.is_revealed() \
                           and not block.is_flagged():
                            self._clicks += 1
                            if self._first_move:
                                if block.is_bomb():
                                    self._board.move_bomb(mouse_x, mouse_y)
                                self._first_move = False
                            self._board.reveal(mouse_x, mouse_y)
                        elif event.button == 1 and block.is_revealed() \
                                and self._jr_reveal:
                            self._clicks += 1
                            for i, j in itertools.product(range(-1, 2), range(-1, 2)):
                                if (
                                    0 <= mouse_x + i < self._width
                                    and 0 <= mouse_y + j < self._height
                                    and not self._board._board[mouse_y + j][mouse_x + i].is_revealed()
                                    and not self._board._board[mouse_y + j][mouse_x + i].is_flagged()
                                ):
                                    self._board.reveal(mouse_x + i, mouse_y + j)
                        elif event.button == 3 and not block.is_revealed():
                            if block.is_flagged():
                                self._flags -= 1
                                block.unflag()
                            else:
                                self._flags += 1
                                block.flag()
                            self._score[0].set_number((self._bombs
                                                       - self._flags) // 100)
                            self._score[1].set_number(((self._bombs
                                                       - self._flags) % 100)
                                                      // 10)
                            self._score[2].set_number((self._bombs
                                                       - self._flags) % 10)

                        elif event.button == 2:
                            if not block.is_flagged():
                                if block.is_question_mark():
                                    self._question_marks -= 1
                                    block.unquestion_mark()
                                else:
                                    self._question_marks += 1
                                    block.question_mark()
                    if mouse_pos[0] < self._smiley.get_position()[0] + 64 and \
                       mouse_pos[0] >= self._smiley.get_position()[0] and \
                       mouse_pos[1] < self._smiley.get_position()[1] + 64 and \
                       mouse_pos[1] >= self._smiley.get_position()[1] and \
                       event.button == 1:
                        self.restart()

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                        input_arr.append("shift")
                    elif (event.key == pygame.K_BACKSPACE and
                          len(input_arr) > 0):
                        input_arr.pop()
                    else:
                        input_arr.append(event.unicode)
                    if len(input_arr) > 7 and \
                       input_arr[-8] == 'x' and input_arr[-7] == 'y' and \
                       input_arr[-6] == 'z' and input_arr[-5] == 'z' and \
                       input_arr[-4] == 'y' and input_arr[-3] == "shift" and \
                       input_arr[-2] == '\r' and input_arr[-1] == '\r':
                        cheat = not cheat
                        input_arr = []

            font = pygame.font.Font(load_file("fonts/minecraft_regular.ttf"),
                                    32)
            text = font.render("".join(input_arr), True, (0, 0, 0))
            screen.blit(text, (50, 750))

            self._board.check_win()

            if self._board._game_over == "WIN":
                self._smiley.set_cool()
                if self._new_highscore:
                    highscores = read_json(load_file("data/data.json"))
                    score_id = len(highscores)
                    summary = {
                        "width": self._width,
                        "height": self._height,
                        "bombs": self._bombs,
                        "clicks": self._clicks,
                        "time": round(self._time, 3)
                    }
                    highscores[score_id] = summary
                    write_json(load_file("data/data.json"), highscores)
                    self._new_highscore = False

            if self._board._game_over == "LOSE":
                if self._play_sound:
                    pygame.mixer.music.load(load_file("sounds/explosion.mp3"))
                    pygame.mixer.music.play()
                    self._play_sound = False
                self._smiley.set_dead()

            if self._board._game_over is None and not self._first_move:
                self._time += 1/60
                self._timer[0].set_number(int(self._time) // 100)
                self._timer[1].set_number((int(self._time) % 100) // 10)
                self._timer[2].set_number(int(self._time) % 10)

            clock.tick(60)

            pygame.display.update()

    def restart(self) -> None:
        self._clicks = 0
        self._flags = 0
        self._question_marks = 0
        self._board = Board(self._width, self._height, self._bombs)
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
        self._score[1].set_number((self._bombs % 100) // 10)
        self._score[2].set_number(self._bombs % 10)
        self._first_move = True
        self._new_highscore = True
        self._play_sound = True


def main():
    pass


if __name__ == "__main__":
    main()
