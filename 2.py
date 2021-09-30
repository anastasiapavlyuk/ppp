import pygame
from pygame.draw import *

pygame.init()

screen = pygame.display.set_mode((800, 400))
polygon(screen, (0, 255, 255), [(0, 0), (800, 0),
                               (800,150), (0,150)], 0)
polygon(screen, (0, 0, 255), [(0, 150), (800, 150),
                               (800,275), (0,275)], 0)
polygon(screen, (255, 255, 0), [(0, 275), (800, 275),
                               (800,400), (0,400)], 0)
circle(screen, (255, 255, 0), (730, 70), 50, 0)
def cloud():
    circle(screen, (255, 255, 255), (60, 60), 20, 0)
    circle(screen, (255, 255, 255), (80, 60), 20, 0)
    circle(screen, (255, 255, 255), (100, 60), 20, 0)
    circle(screen, (255, 255, 255), (75, 75), 20, 0)
    circle(screen, (255, 255, 255), (95, 75), 20, 0)
    circle(screen, (255, 255, 255), (115, 75), 20, 0)
def ship1():
    polygon(screen, (100, 40, 0), [(250, 200), (350, 200),
                                    (350,230), (250,230)], 0)
    polygon(screen, (100, 40, 0), [(350,200), (400, 200),
                                    (350,230), (350, 230)], 0)
    line(screen, (0, 0, 0), (275, 200), (275, 100), 5)                           
    polygon(screen, (100, 100, 100), [(275, 200), (325,150),
                                    (300, 150), (275, 200)], 0)
    polygon(screen, (0, 0, 0), [(275, 200), (325,150),
                                (300, 150), (275, 200)], 2)
    polygon(screen, (100, 100, 100), [(275, 100), (325, 150),
                                    (300, 150), (275, 100)], 0)
    polygon(screen, (0, 0, 0), [(275, 100), (325, 150),
                                (300, 150), (275, 100)], 2)
    circle(screen, (255, 255, 255), (365, 215), 5, 0)
    circle(screen, (255, 255, 255), (365, 215), 5, 2)
ship1()
cloud()



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