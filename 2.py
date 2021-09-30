import pygame
from pygame.draw import *
import tkinter
from math import pi, cos, sin

pygame.init()

screen = pygame.display.set_mode((800, 400))
polygon(screen, (0, 255, 255), [(0, 0), (800, 0),
                               (800,155), (0,155)], 0)
polygon(screen, (0, 0, 255), [(0, 155), (800, 155),
                               (800,290), (0,290)], 0)
polygon(screen, (255, 255, 0), [(0, 290), (800, 290),
                               (800,400), (0,400)], 0)
circle(screen, (255, 255, 0), (730, 70), 50, 0)
def cloud(a,b):
    circle(screen, (255, 255, 255), (60+a, 60+b), 20, 0)
    circle(screen, (255, 255, 255), (80+a, 60+b), 20, 0)
    circle(screen, (255, 255, 255), (100+a, 60+b), 20, 0)
    circle(screen, (255, 255, 255), (75+a, 75+b), 20, 0)
    circle(screen, (255, 255, 255), (95+a, 75+b), 20, 0)
    circle(screen, (255, 255, 255), (115+a, 75+b), 20, 0)
def ship(a):
    
    polygon(screen, (100, 40, 0), [(250+2*a, 200+a/6), (350+3*a, 200+a/6),
                                    (350+3*a,230+a/3), (250+2*a,230+a/3)], 0)                  #cредняя часть
    
    polygon(screen, (100, 40, 0), [(350+3*a,200+a/6), (400+3.5*a, 200+a/6),
                                    (350+3*a,230+a/3), (350+3*a, 230+a/6)], 0)                 #нос
    
    line(screen, (0, 0, 0), (275+2.5*a, 200+a/6), (275+2.5*a, 100-a/6), 5)                     #мачта
    
    polygon(screen, (200, 200, 200), [(275+2.5*a, 200+a/6), (325+2.75*a,150),
                                    (300+2.5*a, 150), (275+2.5*a, 200+a/6)], 0)
    polygon(screen, (0, 0, 0),       [(275+2.5*a, 200+a/6), (325+2.75*a,150),
                                    (300+2.5*a, 150), (275+2.5*a, 200+a/6)], 2)
    polygon(screen, (200, 200, 200), [(275+2.5*a, 100-a/6), (325+2.75*a, 150),
                                    (300+2.5*a, 150), (275+2.5*a, 100-a/6)], 0)
    polygon(screen, (0, 0, 0),       [(275+2.5*a, 100-a/6), (325+2.75*a, 150),
                                    (300+2.5*a, 150), (275+2.5*a, 100-a/6)], 2)                #паруса
    
    circle(screen, (100, 40, 0), [250+2*a, 200+a/6], 30+a/6, 0, draw_bottom_left=True)         #корма        
    circle(screen, (255, 255, 255), (360+3*a, 215+a/4), 5+a/20, 0)                             #какая-то круглая фигня
    circle(screen, (0, 0, 0), (360+3*a, 215+a/4), 5+a/20, 2)

def beach(h):
    a=0
    for i in range(10):
        circle(screen, (255, 255, 0), (0+2*a, 290+h), 40, 0)
        circle(screen, (0, 0, 255), (((80)**2-(2*h)**2)**0.5+2*a, 290-h), 40, 0)
        a+=((80)**2-(2*h)**2)**0.5

def umbrella():
    line(screen, (100, 40, 0), (100, 370+0.5), (100, 210), 6)
    polygon(screen, (255, 192, 203), [(97,210), (103, 210),
                                    (183,250), (17, 250)], 0)
    polygon(screen, (0, 0, 0), [(97,210), (103, 210),
                                    (183,250), (17, 250)], 2)
    a=0
    for i in range(4):
        line(screen, (0, 0, 0), (97,210), (37+a,250), 1)
        a+=20
    b=0
    for i in range(4):
        line(screen, (0, 0, 0), (103,210), (103+b,250), 1)
        b+=20



beach(30)
ship(-10)
ship(100)
cloud(0,0)
cloud(300,40)
cloud(200,-30)
umbrella()


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