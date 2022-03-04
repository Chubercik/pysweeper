from sys import exit

from datatypes import Board, pygame, screen

pygame.init()
pygame.display.set_caption("pysweeper")
pygame.display.set_icon(pygame.image.load("textures/bomb.png"))
clock = pygame.time.Clock()


board = Board(20, 20, 40)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((255, 255, 255))

    board.draw()

    mouse_pos = pygame.mouse.get_pos()
    mouse_x = mouse_pos[0] // 32
    mouse_y = mouse_pos[1] // 32

    m_pos_font = pygame.font.SysFont("Helvetica", 20)
    m_pos_text = m_pos_font.render(f"{mouse_x}, {mouse_y}", True, (0, 0, 0))

    signal = pygame.Surface((32, 32))
    if mouse_x < board.width and mouse_y < board.height:
        screen.blit(m_pos_text, (640, 640))
        if pygame.mouse.get_pressed()[0]:
            board.reveal(mouse_x, mouse_y)
            signal.fill((0, 255, 0))
            screen.blit(signal, (704, 640))
        if pygame.mouse.get_pressed()[2]:
            board.board[mouse_y][mouse_x].flag()
            signal.fill((255, 0, 0))
            screen.blit(signal, (704, 640))
        if pygame.mouse.get_pressed()[1]:
            board.board[mouse_y][mouse_x].question_mark()
            signal.fill((0, 0, 255))
            screen.blit(signal, (704, 640))

    pygame.display.update()
    clock.tick(30)
