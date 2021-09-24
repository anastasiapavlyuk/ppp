import pygame
from pygame.draw import *

pygame.init()

screen = pygame.display.set_mode((500, 400))

circle(screen, (255, 255, 255), (200, 200), 100, 5)
circle(screen, (255, 255, 0), (200, 200), 100, 0)
circle(screen, (255, 0, 0), (160, 175), 25, 0)
circle(screen, (255, 0, 0), (240, 175), 25, 0)
circle(screen, (255, 0, 0), (160, 175), 25, 2)
circle(screen, (255, 0, 0), (240, 175), 25, 2)
circle(screen, (0, 0, 0), (160, 175), 7, 0)
circle(screen, (0, 0, 0), (240, 175), 7, 0)
polygon(screen, (0, 0, 0), [(150, 250), (250, 250),
                               (250,270), (150,270)], 0)

line(screen, (0, 0, 0), (100, 100), (190, 150), 20)
line(screen, (0, 0, 0), (300, 100), (210, 150), 20)


pygame.display.update()
clock = pygame.time.Clock()
finished = True


pygame.display.update()
while finished:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = False

pygame.quit()


