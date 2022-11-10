import itertools
import platform
from sys import exit

from file_io import read_json, write_json
from sprites import load_file
from utilities import Board, Button, Smiley, Timer, pg, prompt_file, screen

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
        self.width = width
        self.height = height
        self.clicks = 0
        self.flags = 0
        self.question_marks = 0
        self.board = Board(width, height, bombs)
        self.bombs = self.board.bomb_count
        self.smiley = Smiley(x=(self.board.left_offset - 32
                                + 32*self.width//2),
                             y=(self.board.top_offset - 64))
        self.time: float = 0
        self.timer_0 = Timer(x=(self.board.left_offset + 32
                                + 32*self.width//2),
                             y=(self.board.top_offset - 64))
        self.timer_1 = Timer(x=(self.board.left_offset + 64
                                + 32*self.width//2),
                             y=(self.board.top_offset - 64))
        self.timer_2 = Timer(x=(self.board.left_offset + 96
                                + 32*self.width//2),
                             y=(self.board.top_offset - 64))
        self.timer = [self.timer_0, self.timer_1, self.timer_2]
        self.score_0 = Timer(x=(self.board.left_offset - 128
                                + 32*self.width//2),
                             y=(self.board.top_offset - 64))
        self.score_1 = Timer(x=(self.board.left_offset - 96
                                + 32*self.width//2),
                             y=(self.board.top_offset - 64))
        self.score_2 = Timer(x=(self.board.left_offset - 64
                                + 32*self.width//2),
                             y=(self.board.top_offset - 64))
        self.score = [self.score_0, self.score_1, self.score_2]
        self.score[0].number = (self.bombs // 100)
        self.score[1].number = ((self.bombs % 100) // 10)
        self.score[2].number = (self.bombs % 10)
        self.button_test = Button(self.board.left_offset - 125,
                                  self.board.top_offset,
                                  100, 50)
        self.button_1 = Button(self.board.left_offset - 125,
                               self.board.top_offset + 55,
                               100, 50)
        self.button_2 = Button(self.board.left_offset - 125,
                               self.board.top_offset + 110,
                               100, 50)
        self.button_3 = Button(self.board.left_offset - 125,
                               self.board.top_offset + 165,
                               100, 50)
        self.first_move = True
        self.play_sound = True
        self.new_highscore = True
        self.jr_reveal = jr_reveal

    def run(self) -> None:
        pg.init()
        pg.mixer.init()

        pg.display.set_caption("pysweeper")
        pg.display.set_icon(pg.image.load(load_file("textures/icon.png")))
        pg.display.set_mode(size=(32*self.width + 2*self.board.left_offset,
                                  32*self.height + 2*self.board.top_offset),
                            flags=pg.RESIZABLE,
                            vsync=True)

        ###
        import pygame_gui as pgui

        manager = pgui.UIManager((32*self.width + 2*self.board.left_offset,
                                  32*self.height + 2*self.board.top_offset))

        hello_button = pgui.elements.UIButton(relative_rect=pg.Rect((self.board.left_offset - 125, self.board.top_offset + 220), (-1, 50)),
                                              text="Hello World",
                                              manager=manager,
                                              object_id=pgui.core.ObjectID(class_id="@friendly_buttons",
                                              object_id="#hello_button"))
        ###

        clock = pg.time.Clock()

        if sys_name == "Windows":
            temp = win32gui.GetPixel(dc, 0, 0)

        input_arr = []
        cheat = False

        font = pg.font.Font(load_file("fonts/minecraft_regular.ttf"), 32)

        while True:
            screen.fill((170, 170, 170))

            self.board.draw()
            self.smiley.draw(screen)
            for timer in self.timer:
                timer.draw(screen)
            for score in self.score:
                score.draw(screen)

            mouse_pos = pg.mouse.get_pos()
            mouse_x = (mouse_pos[0] - self.board.left_offset) // 32
            mouse_y = (mouse_pos[1] - self.board.top_offset) // 32

            if cheat and sys_name == "Windows" and \
               mouse_x < self.width and mouse_x >= 0 and \
               mouse_y < self.height and mouse_y >= 0 and \
               not self.board.board[mouse_y][mouse_x].is_bomb:
                win32gui.SetPixel(dc, 0, 0, white)
            elif sys_name == "Windows":
                win32gui.SetPixel(dc, 0, 0, temp)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    self.smiley.set_in_awe()
                    if self.button_test.is_mouse_over(mouse_pos) and \
                       event.button == 1:
                        self.button_test.button_clicked = 1

                if event.type == pg.MOUSEBUTTONUP:
                    self.smiley.set_reset()
                    if mouse_x < self.width and \
                       mouse_x >= 0 and \
                       mouse_y < self.height and \
                       mouse_y >= 0 and \
                       self.board.game_over is None:
                        block = self.board.board[mouse_y][mouse_x]
                        if event.button == 1 and not block.is_revealed \
                           and not block.is_flagged:
                            pg.mixer.music.load(load_file("sounds/plop.mp3"))
                            pg.mixer.music.play()
                            self.clicks += 1
                            if self.first_move:
                                if block.is_bomb:
                                    self.board.move_bomb(mouse_x, mouse_y)
                                self.first_move = False
                            self.board.reveal(mouse_x, mouse_y)
                        elif event.button == 1 and block.is_revealed \
                                and self.jr_reveal:
                            pg.mixer.music.load(load_file("sounds/plop.mp3"))
                            pg.mixer.music.play()
                            self.clicks += 1
                            for i, j in itertools.product(range(-1, 2), range(-1, 2)):
                                if (
                                    0 <= mouse_x + i < self.width
                                    and 0 <= mouse_y + j < self.height
                                    and not self.board.board[mouse_y + j][mouse_x + i].is_revealed
                                    and not self.board.board[mouse_y + j][mouse_x + i].is_flagged
                                ):
                                    self.board.reveal(mouse_x + i, mouse_y + j)
                        elif event.button == 3 and not block.is_revealed:
                            if block.is_flagged:
                                self.flags -= 1
                                block.is_flagged = False
                            else:
                                self.flags += 1
                                block.is_flagged = True
                            self.update_score()
                        elif event.button == 2:
                            if not block.is_flagged:
                                if block.is_question_mark:
                                    self.question_marks -= 1
                                    block.is_question_mark = False
                                else:
                                    self.question_marks += 1
                                    block.is_question_mark = True
                    if mouse_pos[0] < self.smiley.get_position()[0] + 64 and \
                       mouse_pos[0] >= self.smiley.get_position()[0] and \
                       mouse_pos[1] < self.smiley.get_position()[1] + 64 and \
                       mouse_pos[1] >= self.smiley.get_position()[1] and \
                       event.button == 1:
                        self.restart()

                    if self.button_test.is_mouse_over(mouse_pos) and \
                       event.button == 1:
                        self.button_test.button_clicked = 0
                        # self.button_test.button_clicked = clock.get_fps()//20

                        # horrible practice, but at least
                        # it'll stop the game from crashing
                        # FIX THIS LATER
                        try:
                            input_arr.extend(str(read_json(prompt_file(load_file("icon.ico") if sys_name == "Windows" else None))))
                        except Exception as e:
                            print(e)

                    if self.button_1.is_mouse_over(mouse_pos) and \
                       event.button == 1:
                        self.button_1.button_clicked = int(clock.get_fps()//20)
                        input_arr.append('1')

                    if self.button_2.is_mouse_over(mouse_pos) and \
                       event.button == 1:
                        self.button_2.button_clicked = int(clock.get_fps()//20)
                        input_arr.append('2')

                    if self.button_3.is_mouse_over(mouse_pos) and \
                       event.button == 1:
                        self.button_3.button_clicked = int(clock.get_fps()//20)
                        input_arr.append('3')

                if event.type == pg.KEYDOWN:
                    if event.key in (pg.K_LSHIFT, pg.K_RSHIFT):
                        input_arr.append("shift")
                    elif (event.key == pg.K_BACKSPACE and
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

                if event.type == pg.VIDEORESIZE:
                    # disallow resizing to smaller
                    # dimensions than the board size
                    self.screen = pg.display.set_mode((max(event.w, self.width*32),
                                                       max(event.h, self.height*32)),
                                                      pg.RESIZABLE)
                    self.resize()

                ###
                if event.type == pgui.UI_BUTTON_PRESSED:
                    if event.ui_element == hello_button:
                        input_arr.extend("Hello World!")

                manager.process_events(event)
                ###

            text = font.render("".join(input_arr), True, (0, 0, 0))
            screen.blit(text, (self.board.left_offset - 125, self.board.top_offset + self.board.height*32 + 50))

            self.board.check_win()

            if self.board.game_over == "WIN":
                self.smiley.set_cool()
                if self.new_highscore:
                    highscores = read_json(load_file("data/data.json"))
                    score_id = len(highscores)
                    summary = {
                        "width": self.width,
                        "height": self.height,
                        "bombs": self.bombs,
                        "clicks": self.clicks,
                        "time": round(self.time, 3)
                    }
                    highscores[score_id] = summary
                    write_json(load_file("data/data.json"), highscores)
                    self.new_highscore = False

            if self.board.game_over == "LOSE":
                if self.play_sound:
                    pg.mixer.music.load(load_file("sounds/explosion.mp3"))
                    pg.mixer.music.play()
                    self.play_sound = False
                self.smiley.set_dead()

            if self.board.game_over is None and not self.first_move:
                self.time += 1/60
                self.timer[0].number = (int(self.time) // 100)
                self.timer[1].number = ((int(self.time) % 100) // 10)
                self.timer[2].number = (int(self.time) % 10)

            if self.button_test.button_clicked > 0:
                self.button_test.draw(screen, "test",
                                      (0, 0, 0), (255, 255, 255),
                                      font)
                # self.button_test.button_clicked -= 1
            else:
                self.button_test.draw(screen, "test",
                                      (255, 255, 255), (0, 0, 0),
                                      font)

            if self.button_1.button_clicked > 0:
                self.button_1.draw(screen, '1',
                                   (0, 0, 0), (255, 255, 255),
                                   font)
                self.button_1.button_clicked -= 1
            else:
                self.button_1.draw(screen, '1',
                                   (255, 255, 255), (0, 0, 0),
                                   font)

            if self.button_2.button_clicked > 0:
                self.button_2.draw(screen, '2',
                                   (0, 0, 0), (255, 255, 255),
                                   font)
                self.button_2.button_clicked -= 1
            else:
                self.button_2.draw(screen, '2',
                                   (255, 255, 255), (0, 0, 0),
                                   font)

            if self.button_3.button_clicked > 0:
                self.button_3.draw(screen, '3',
                                   (0, 0, 0), (255, 255, 255),
                                   font)
                self.button_3.button_clicked -= 1
            else:
                self.button_3.draw(screen, '3',
                                   (255, 255, 255), (0, 0, 0),
                                   font)

            # clock.tick(60)

            ###
            pg.display.set_caption(f"pysweeper {clock.get_fps():.2f}")

            time_delta = clock.tick(60)/1000.0
            manager.update(time_delta)

            manager.draw_ui(screen)
            ###

            pg.display.update()

    def restart(self) -> None:
        self.clicks = 0
        self.flags = 0
        self.question_marks = 0
        temp_left_offset = self.board.left_offset
        temp_top_offset = self.board.top_offset
        self.board = Board(self.width, self.height, self.bombs)
        self.board.left_offset = temp_left_offset
        self.board.top_offset = temp_top_offset
        self.board.window_resize()
        self.smiley = Smiley(x=(self.board.left_offset - 32
                                + 32*self.width//2),
                             y=(self.board.top_offset - 64))
        self.time = 0
        self.set_digit_displays()
        self.score[0].number = (self.bombs // 100)
        self.score[1].number = ((self.bombs % 100) // 10)
        self.score[2].number = (self.bombs % 10)
        self.first_move = True
        self.new_highscore = True
        self.play_sound = True

    def resize(self) -> None:
        self.board.left_offset = (pg.display.get_surface().get_width() -
                                  32*self.width)//2
        self.board.top_offset = (pg.display.get_surface().get_height() -
                                 32*self.height)//2
        self.smiley = Smiley(x=(self.board.left_offset - 32
                                + 32*self.width//2),
                             y=(self.board.top_offset - 64))
        self.button_test.set_position(self.board.left_offset - 125, self.board.top_offset)
        self.button_1.set_position(self.board.left_offset - 125, self.board.top_offset + 55)
        self.button_2.set_position(self.board.left_offset - 125, self.board.top_offset + 110)
        self.button_3.set_position(self.board.left_offset - 125, self.board.top_offset + 165)
        self.set_digit_displays()
        self.update_score()
        self.board.window_resize()

    def set_digit_displays(self):
        self.timer_0 = Timer(x=(self.board.left_offset
                                + 32 + 32 * self.width // 2),
                             y=self.board.top_offset - 64)

        self.timer_1 = Timer(x=(self.board.left_offset
                                + 64 + 32 * self.width // 2),
                             y=self.board.top_offset - 64)

        self.timer_2 = Timer(x=(self.board.left_offset
                                + 96 + 32 * self.width // 2),
                             y=self.board.top_offset - 64)
        self.timer = [self.timer_0, self.timer_1, self.timer_2]

        self.score_0 = Timer(x=(self.board.left_offset
                                - 128 + 32 * self.width // 2),
                             y=self.board.top_offset - 64)

        self.score_1 = Timer(x=(self.board.left_offset
                                - 96 + 32 * self.width // 2),
                             y=self.board.top_offset - 64)

        self.score_2 = Timer(x=(self.board.left_offset
                                - 64 + 32 * self.width // 2),
                             y=self.board.top_offset - 64)
        self.score = [self.score_0, self.score_1, self.score_2]

    def update_score(self):
        self.score[0].number = ((((self.bombs - self.flags)) // 100))
        self.score[1].number = (((((self.bombs - self.flags)) % 100) // 10))
        self.score[2].number = ((((self.bombs - self.flags)) % 10))


def main() -> None:
    pass


if __name__ == "__main__":
    main()
