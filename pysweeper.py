from sys import exit

from datatypes import Board, pygame, screen


class Pysweeper:
    def __init__(self, width: int, height: int, bombs: int):
        self.width = width
        self.height = height
        self.bombs = bombs
        self.clicks = 0
        self.flags = 0
        self.question_marks = 0
        self.board = Board(width, height, bombs)

    def run(self):
        pygame.init()
        pygame.display.set_caption("pysweeper")
        pygame.display.set_icon(pygame.image.load("textures/bomb.png"))
        clock = pygame.time.Clock()
        pygame.display.set_mode(size=(32*self.width + 96, 32*self.height + 32))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            screen.fill((255, 255, 255))

            self.board.draw()

            mouse_pos = pygame.mouse.get_pos()
            mouse_x = mouse_pos[0] // 32
            mouse_y = mouse_pos[1] // 32

            text_font = pygame.font.SysFont("Helvetica", 20)
            m_pos_text = text_font.render(f"{mouse_x}, {mouse_y}",
                                          True,
                                          (0, 0, 0))

            signal = pygame.Surface((32, 32))
            if mouse_x < self.width and mouse_y < self.height:
                screen.blit(m_pos_text, (32*self.width, 32*self.height))
                if pygame.mouse.get_pressed()[0]:
                    self.clicks += 1
                    self.board.reveal(mouse_x, mouse_y)
                    signal.fill((0, 255, 0))
                    screen.blit(signal, (32*self.width + 64, 32*self.height))
                if pygame.mouse.get_pressed()[2]:
                    if self.board.board[mouse_y][mouse_x].is_flagged:
                        self.flags -= 1
                        self.board.board[mouse_y][mouse_x].unflag()
                    else:
                        self.flags += 1
                        self.board.board[mouse_y][mouse_x].flag()
                    signal.fill((255, 0, 0))
                    screen.blit(signal, (32*self.width + 64, 32*self.height))
                if pygame.mouse.get_pressed()[1]:
                    if self.board.board[mouse_y][mouse_x].is_question_mark:
                        self.question_marks -= 1
                        self.board.board[mouse_y][mouse_x].unquestion_mark()
                    else:
                        self.question_marks += 1
                        self.board.board[mouse_y][mouse_x].question_mark()
                    signal.fill((0, 0, 255))
                    screen.blit(signal, (32*self.width + 64, 32*self.height))

            fps_counter = text_font.render(f"FPS: {int(clock.get_fps())}",
                                           True,
                                           (0, 0, 0))
            screen.blit(fps_counter, (32*self.width, 0))

            num_flags = text_font.render(f"Flags: {self.flags}",
                                         True,
                                         (0, 0, 0))
            screen.blit(num_flags, (32*self.width, 32))

            pygame.display.update()
            clock.tick(60)


def main():
    pass


if __name__ == "__main__":
    main()
