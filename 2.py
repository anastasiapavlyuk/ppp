import pygame
from pygame.draw import *
import tkinter
import numpy as np
from math import pi, cos, sin

pygame.init()
WHITE=(255,255,255)
BLACK=(0, 0, 0)
GREY=(200, 200, 200)
LBLUE=(0, 255, 255)
BLUE=(0, 0, 255)
YELLOW=(255, 255, 0)
BROWN=(100, 40, 0)
PINK=(255, 192, 203)
screen = pygame.display.set_mode((800,400))
def background(x,y,y0,y1):
    '''Функция background рисует фон. 
   :param:x ширина картинки
   :param:y высота картинки
   :param:y0 уровень горизонта
   :param:y1 - уровень пляжа''' 
    polygon(screen, LBLUE, [(0, 0), (x, 0),
                               (x,y0), (0,y0)], 0)
    polygon(screen, BLUE, [(0, y0), (x, y0),
                               (x,y1), (0,y1)], 0)
    polygon(screen, YELLOW, [(0, y1), (x, y1),
                               (x,y), (0,y)], 0)

def sun(x,y,r,n):
    '''Функция sun рисует солнце.
    :param:x координата x
    :param:y координата y
    :param:r-радиус
    :param:n-количество лучей
    '''
    circle(screen, YELLOW, (x, y), r, 0)
    pfi=0
    m = []
    for f in range(n):
        m.append([x+(r+5*(-1)**f)*np.cos(pfi), y+(r+5*(-1)**f)*np.sin(pfi)])
        pfi+=2*np.pi/n
    polygon(screen, YELLOW, m, 0)

def cloud(a,b):
    '''Функция cloud рисует облако.
     :param:a координата x
     :param:b координата y'''
    circle(screen, WHITE, (60+a, 60+b), 20, 0)
    circle(screen, WHITE, (80+a, 60+b), 20, 0)
    circle(screen, WHITE, (100+a, 60+b), 20, 0)
    circle(screen, WHITE, (75+a, 75+b), 20, 0)
    circle(screen, WHITE, (95+a, 75+b), 20, 0)
    circle(screen, WHITE, (115+a, 75+b), 20, 0)

def ship(a,x,y):
   '''Функция ship0 рисует корабль. 
   :param:x координата центральной точки по x 
   :param:y координааы центральной точки по y 
   :param:a - масштаб'''
   polygon(screen, BROWN, [(x-a,y-a/5), (x+a,y-a/5),(x+a, y+a/5), (x-a, y+a/5)], 0)              #cредняя часть   
   polygon(screen, BROWN, [(x+a,y-a/5),(x+a*1.8,y-a/5),(x+a, y+a/5)], 0)                 #нос
   line(screen, BLACK, (x-0.2*a, y-a/5), (x-0.2*a, y-1.5*a), 5)                     #мачта
   polygon(screen, GREY, [(x-0.2*a, y-a/5),(x+a*0.6, y-0.875*a), (x-0.2*a, y-1.5*a),(x+a/5, y-0.875*a)], 0) #паруса
   polygon(screen, BLACK,       [(x-0.2*a, y-a/5),(x+a*0.6, y-0.875*a), (x-0.2*a, y-1.5*a),(x+a/5, y-0.875*a)], 2)
   line(screen, BLACK, (x+a/5, y-0.875*a),(x+a*0.6, y-0.875*a), 2)
   circle(screen, BROWN, [x-a,y-a/5], a*0.4, 0, draw_bottom_left=True)         #корма        
   circle(screen, WHITE, (x+a*1.1, y), a*0.1, 0)                             #окошечко
   circle(screen, BLACK, (x+a*1.1, y), a*0.1, 2)

def beach(h):
    '''Функция beach рисует пляж.
    :param:h определяет радиус кривизны волн'''
    a=0
    for i in range(10):
        circle(screen, YELLOW, (0+2*a, 290+h), 40, 0)
        circle(screen, BLUE, (((80)**2-(2*h)**2)**0.5+2*a, 290-h), 40, 0)
        a+=((80)**2-(2*h)**2)**0.5

def umbrella(x,y,t):
    '''Функция umbrella рисует зонт. 
    :param:x координата верхней точки по x 
    :param:y координааы верхней точки по y 
    :param:t - масштаб'''
    line(screen, BROWN, (x, y), (x,y+40*t), t)
    polygon(screen,PINK , [[x+4,y],[x+10*t, y+10*t],[x-10*t, y+10*t], [x-4,y]], 0)
    polygon(screen, BLACK, [[x+4,y],[x+10*t, y+10*t,],[x-10*t, y+10*t], [x-4,y]], 2)
    a=0
    for i in range(4):
        line(screen, BROWN, (x-4,y), (x-10*t+a, y+10*t), 1)
        a+=3*t
    b=0
    for i in range(4):
        line(screen, BROWN, (x+4,y), (x+10*t-b,y+10*t), 1)
        b+=3*t

def picture(x,y):
    '''Функция picture рисует картинку.(пляж,солнце,2 кораблика,2 облака,2 зонтика) 
    :param:x ширина рисунка 
    :param:y высота рисунка '''
    background(x,y,155,290)
    sun(730,70,40,110)
    beach(30)
    ship(60,300,170)
    ship(100,600,200)
    cloud(0,0)
    cloud(300,40)
    cloud(200,-30)
    umbrella(100,210,6)
    umbrella(200,260,3)

picture(800,400)

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