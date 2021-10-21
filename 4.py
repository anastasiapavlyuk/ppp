from turtle import tracer
import json
import pygame
from pygame.constants import K_ESCAPE, QUIT
from pygame.draw import *
from random import randint
pygame.init()

FPS = 60
screen = pygame.display.set_mode((1200, 700))
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

N = 8

x = [0]*N; y = [0]*N; r = [0]*N; color = [BLACK]*N; t = [0]*N; vx = [0]*N; vy = [0]*N
def new_ball(i):
    t[i] = randint(120,1200)
    x[i] = randint(100, 1100)
    y[i] = randint(100, 900)
    r[i] = randint(10, 50)
    vx[i] = randint(-5,5)
    vy[i] = randint(-5,5)
    color[i] = COLORS[randint(0, 5)]

M = 7
X = [0]*N; Y = [0]*N; a = [0]*N; Color = [BLACK]*N; T = [0]*N; Vx = [0]*N; Vy = [0]*N
def new_square(i):
    a[i] = randint(10, 50)
    T[i] = randint(120,1200)
    X[i] = randint(50, 1150)
    Y[i] = randint(50, 950)
    Color[i] = COLORS[randint(0, 5)]

for i in range(N):
    new_ball(i)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

x1=0
y1=0

n=0

tx = pygame.font.Font(None, 40)
rx = tx.render('score:' + str(n), True, (255,255,0))

time = 0
end = 0

max_score = -1

Name = ""



while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            finished = True
        
        elif event.type == pygame.KEYDOWN:
            if time > 1800 and end !=1:
                if event.key!= 8 and event.key != 13 and event.key!= pygame.K_ESCAPE:
                    Name = Name + event.unicode
                if event.key == 8:
                    Name = Name[:-1]
                if event.key == 13:
    
                    l["data"].append({"name": Name, "points": n})
                    
                    table = []
                    names = []
                    for i in res:
                        table.append(i["points"])
                        names.append(i["name"])
                    A = len(table)
                    for i in range (A-1):
                        for j in range (A-i-1):
                            if table[j] < table[j+1]:
                                table[j], table[j+1] = table[j+1], table[j]
                                names[j], names[j+1] = names[j+1], names[j]
                    Z = 0
                    for i in res:
                        i["points"] = table[Z]
                        i["name"] = names[Z]
                        Z+=1
                    
                    with open('data.JSON','w') as f:
                        json.dump(l, f)
                        
                    f.close()
                    end += 1
            if event.key == pygame.K_ESCAPE:
                finished = True
        elif time <= 1800 and  event.type == pygame.MOUSEBUTTONDOWN:
            (x1, y1) = event.pos
            for i in range(N):
                if ((x[i]-x1)**2+(y[i]-y1)**2)**0.5 <= r[i]:
                    n+=50//r[i]
                    t[i]=0
            for i in range(M):
                if X[i]-a[i]/2<x1 and x1<X[i]+a[i]/2 and Y[i]-a[i]/2<y1 and y1<Y[i]+a[i]/2:
                    n+=1
                    T[i]=0
    for i in range(N):                          #пробегаемся по массиву шариков 
        if t[i]==0:                             
            new_ball(i)                         #если шарик умер, создаем новый
        if x[i]<r[i] or x[i]>1200-r[i]:         #проверяем, что он не вылетел за поле / возвращаем обратно
            if vx[i] < 0:
                vx[i] = -vx[i] + 1
            else:
                vx[i] = -vx[i] - 1
            if x[i]<r[i]:
                x[i]=r[i]
            elif x[i]>1200-r[i]:
                x[i]=1200-r[i]
        if y[i]<r[i] or y[i]>700-r[i]:
            if vy[i] > 0:
                vy[i] = -vy[i] - 1
            else:
                vy[i] = -vy[i] +1
            if y[i]<r[i]:
                y[i]=r[i]
            elif y[i]>700-r[i]:
                y[i]=700-r[i]
        x[i]+=vx[i]                             
        y[i]+=vy[i]
        t[i]-=1
        circle(screen, color[i], (x[i], y[i]), r[i])  
    for i in range(M):
        if T[i] == 0:
            new_square(i)
        polygon(screen, Color[i], [[X[i]-a[i]/2, Y[i]-a[i]/2], [X[i]+a[i]/2, Y[i]-a[i]/2],
                                [X[i]+a[i]/2, Y[i]+a[i]/2], [X[i]-a[i]/2, Y[i]+a[i]/2]], 2)
        T[i]-=1
    time +=1
    end_text = tx.render('Game over', True, (255, 255, 255))
    leaderboard = tx.render('Leaderboard:', True, (255, 255, 255))
    name_text = tx.render(Name, True, (255, 255, 255))
    rx = tx.render('score:' + str(n), True, (255,255,0))
    if time > 1800 and end != 1:
        screen.blit(rx, (550,350))
        screen.blit(name_text, (525, 375))
       
    with open('data.JSON','r') as f:
        l = json.load(f)
    f.close()
    res = l['data']
    for record in res:
        if record["points"] > max_score:
            max_score = record["points"]
            max_data = record
    c = 0
    if end == 1:
        screen.blit(end_text, (530, 375))
        screen.blit(leaderboard, (530, 400))
        for i in res:
            man = tx.render(i["name"] + " " + str(i["points"]), True, (255, 255, 255))
            screen.blit(man, (530, 425 + 25*c))
            c+=1
        #leader = tx.render(max_data["name"] + " " + str(max_data["points"]), True, (255, 255, 255))
        #screen.blit(leader, (530, 425))

    if time <= 1800:
        screen.blit(rx, (50,100))   
    pygame.display.update()
    screen.fill(BLACK)





pygame.quit()