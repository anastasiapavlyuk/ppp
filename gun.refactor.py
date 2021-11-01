import math
from random import randint, choice

import pygame


FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

def norm(p1, p2, v):
    ''' Приведение скорости к нужному значению '''
    l = math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
    return (p2[0]-p1[0])*v/l, (p2[1]-p1[1])*v/l

class Ball:
    def __init__(self, screen: pygame.Surface, x, y):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.g = 1
        self.color = choice(GAME_COLORS)
        self.life_time = 120
        self.cur_time = 0
        self.fric = 0.6

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.x < self.r:
            self.x = self.r
            self.vx *= -self.fric
            self.vy *= self.fric
        elif self.x > WIDTH - self.r:
            self.x = WIDTH - self.r
            self.vx *= -self.fric
            self.vy *= self.fric

        if self.y < self.r:
            self.y = self.r
            self.vy *= -self.fric
            self.vx *= self.fric
        elif self.y > HEIGHT - self.r:
            self.y = HEIGHT - self.r
            self.vy *= -self.fric
            self.vx *= self.fric

        self.vy += self.g
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

        self.cur_time += 1

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if math.sqrt((self.x - obj.x)**2 + (self.y - obj.y)**2) <= self.r + obj.r:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 50
        self.y = HEIGHT - 45
        self.length = 50
        self.thik = 5

        self.v = 3

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x + self.length*math.cos(self.an), self.y + self.length*math.sin(self.an))
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0] >= self.x:
                try:
                    self.an = math.atan((event.pos[1]-self.y) / (event.pos[0]-self.x))
                except: pass
            else:
                self.an = math.pi + math.atan((event.pos[1]-self.y) / (event.pos[0]-self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        vert = [
            (self.x - self.thik*math.sin(-self.an), self.y - self.thik*math.cos(-self.an)),
            (self.x + self.length*math.cos(-self.an) - self.thik*math.sin(-self.an), self.y - self.length*math.sin(-self.an) - self.thik*math.cos(-self.an)),
            (self.x + self.length*math.cos(-self.an) + self.thik*math.sin(-self.an), self.y - self.length*math.sin(-self.an) + self.thik*math.cos(-self.an)),
            (self.x + self.thik*math.sin(-self.an), self.y + self.thik*math.cos(-self.an))
        ]
        ''' Отрисовка пушки '''
        pygame.draw.polygon(self.screen, self.color, vert)
        pygame.draw.rect(self.screen, GREEN, (self.x - 35, self.y, 70, 30))
        pygame.draw.circle(self.screen, BLACK, (self.x - 35, self.y + 30), 15)
        pygame.draw.circle(self.screen, BLACK, (self.x + 35, self.y + 30), 15)

        

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 50:
                self.f2_power += 0.5
            self.color = RED
        else:
            self.color = GREY

    def move(self, dir):
        if dir == 'left':
            self.x -= self.v
        else:
            self.x += self.v


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.life_time = 450
        self.cur_time = 0
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.cur_time = 0
        self.n = randint(2, 5)
        self.count = 1
        print(self.n)
        
        if self.n == 2:
            self.move_r = randint(200, 300)
        else:
            self.move_r = randint(50, 100)

        self.center_x = randint(self.move_r, WIDTH - self.move_r)
        self.center_y = randint(self.move_r, HEIGHT - self.move_r)
        self.trag_points = []

        self.r = randint(10, 40)
        self.color = choice([RED, GREEN, GREY, CYAN])
        
        a = 0
        phi = 2*math.pi/self.n
        
        while a < 2*math.pi:
            self.trag_points.append((self.center_x + self.move_r*math.cos(a), self.center_y - self.move_r*math.sin(a)))
            a += phi
        
        self.x = self.trag_points[0][0]
        self.y = self.trag_points[0][1]

        self.v = randint(1, 3)
        self.vx, self.vy = norm(self.trag_points[0], self.trag_points[1], self.v)
        print(self.trag_points)

    def update_speed(self):
        self.vx, self.vy = norm(self.trag_points[self.count-1], self.trag_points[self.count], self.v)

    def hit(self):
        """Попадание шарика в цель."""
        global points
        points += 1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

        self.cur_time += 1

    def move(self):
        dr = 10
        if math.sqrt((self.x - self.trag_points[self.count][0])**2 + (self.y - self.trag_points[self.count][1])**2) <= dr:
            self.x = self.trag_points[self.count][0]
            self.y = self.trag_points[self.count][1]
            self.count += 1
            if self.count == self.n:
                self.count = 0
            self.update_speed()

        self.x += self.vx
        self.y += self.vy
        

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 30)

bullet = 0
points = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
targets = [Target(screen), Target(screen), Target(screen)]
finished = False

while not finished:
    screen.fill(WHITE)

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    if pygame.key.get_pressed()[pygame.K_LEFT]:
        gun.move('left')
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        gun.move('right')

    for b in balls:
        b.draw()
        b.move()
        for t in targets:
            if b.hittest(t):
                t.hit()
                t.new_target()
        if b.cur_time == b.life_time:
            balls.remove(b)
        

    gun.power_up()

    gun.draw()
    for t in targets:
        if t.cur_time == t.life_time:
                t.new_target()
        t.move()
        t.draw()

    score_text = font.render('Счет:'+str(points), True, (0, 0, 0))
    screen.blit(score_text, (15, 15))

    pygame.display.update()


pygame.quit()
