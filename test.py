import pygame


WIDTH = 640
HEIGHT = 480
FPS = 144

# initialize pygame and create window
pygame.init()
pygame.mixer.init()  # for sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("<Your game>")
clock = pygame.time.Clock()  # for syncing the FPS


# group all the sprites together for ease of update
all_sprites = pygame.sprite.Group()

# game loop
running = True
bg_color = (0, 0, 0)
while running:

    # 1 process input/events
    clock.tick(FPS)  # will make the loop run at the same speed all the time
    for event in pygame.event.get():  # gets all the events which have occured till now and keeps tab of them
        # listening for the X button at the top
        if event.type == pygame.QUIT:
            running = False

    # 2 update
    all_sprites.update()

    # 3 draw/render
    screen.fill(bg_color)
    if bg_color[0] <= 0:
        r_switch = 1
    if bg_color[1] <= 0:
        g_switch = 1
    if bg_color[2] <= 0:
        b_switch = 1
    if bg_color[0] >= 255:
        r_switch = -1
    if bg_color[1] >= 255:
        b_switch = -1
    if bg_color[2] >= 255:
        g_switch = -1
    new_r = max(min(bg_color[0] + 1*r_switch, 255), 0)
    new_g = max(min(bg_color[1] + 1*g_switch, 255), 0)
    new_b = max(min(bg_color[2] + 1*b_switch, 255), 0)
    bg_color = (new_r, new_g, new_b)

    all_sprites.draw(screen)

    # done after drawing everything to the screen
    pygame.display.flip()

pygame.quit()
