import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("pysweeper")
pygame.display.set_icon(pygame.image.load("textures/bomb.png"))
clock = pygame.time.Clock()

smiley = pygame.image.load("textures/smiley.png")

x = 0
y = 0
x_switch = 1
y_switch = 1

scale = 2

# rotation is weird so I'm not doing it rn

test_font = pygame.font.Font("fonts/minecraft_regular.ttf", 20)
text_surface = test_font.render("Hello World!", False, (0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((255, 255, 255))

    smiley_sca = pygame.transform.scale(smiley,
                                        (smiley.get_width()*scale,
                                         smiley.get_height()*scale))

    if x > 800 - smiley.get_width()*scale:
        x_switch = -1
    if x < 0:
        x_switch = 1
    if y > 400 - smiley.get_height()*scale:
        y_switch = -1
    if y < 0:
        y_switch = 1
    x += x_switch
    y += y_switch

    screen.blit(text_surface, (10, 10))
    screen.blit(smiley_sca, (x, y))
    pygame.display.update()
    clock.tick(144)
