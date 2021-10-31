from random import randrange as rnd, choice
from random import random
import tkinter as tk
import math
import time

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)
canv.focus_set()


class target():
    def __init__(self):
        """
        Конструктор класса Target
        """
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        self.x = 0
        self.y = 0
        self.r = 0
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)

    def hit(self):
        """Попадание шарика в цель. Она перемещается в невидимую часть экрана"""
        canv.coords(self.id, -10, -10, -10, -10)


# Дочерний класс класса target, двигающийся по восьмёрке-лисажу
class lissajou_target(target):
    def __init__(self):
        """
        Инициализация класса целей, двигающихся по восмьёрке
        """
        target.__init__(self)
        # Амплитуды колебания по восьмёрки для разных осей
        self.a_x = 0
        self.a_y = 0
        # Переменные, хранящие координаты центра восьмёрки
        self.x_0 = self.x
        self.y_0 = self.y
        # Переменная времени, благодаря которой считается положение цели в конкретный момент
        self.t = 0
        # Переменная шага дискретизация движения цели
        self.dt = 0.5
        # Переменная частоты, с которой колеблется по осям цель
        self.freq = 1
        # Переменная цвета цели
        self.colour = choice(['red', '#ff7f50', 'blue', 'green', '#b666d2', 'yellow', 'cyan', '#ffbf00', '#711919'])
        canv.itemconfig(self.id, fill=self.colour)

    def new_target(self, x_min=0, x_max=800, y_min=0, y_max=600):
 
        # Задание новых характеристик траектории цели
        self.a_x = rnd(70, 120)
        self.a_y = rnd(70, 120)
        self.r = rnd(5, 50)
        self.x_0 = rnd(x_min + self.r + self.a_x, x_max - self.r - self.a_x)
        self.y_0 = rnd(y_min + self.r + self.a_y, y_max - self.r - self.a_y)
        self.freq = random() * 0.2 + 0.05
        # Обнуление переменной времени
        self.t = 0
        canv.coords(self.id, self.x_0 - self.r, self.y_0 - self.r, self.x_0 + self.r, self.y_0 + self.y_0)

    def move(self):

        # Обновление переменной времени
        self.t += self.dt
        # Обновление координат цели
        self.x = self.x_0 + self.a_x * math.cos(self.freq * self.t)
        self.y = self.y_0 + self.a_y * math.sin(2 * self.freq * self.t)
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )


# Класс цели, двигающейся равномерно с отражением от границ экрана
class uniform_moving_target(target):
    def __init__(self):
        target.__init__(self)
        self.vx = 0
        self.vy = 0
        self.colour = choice(['red', '#ff7f50', 'blue', 'green', '#b666d2', 'yellow', 'cyan', '#ffbf00', '#711919'])
        canv.itemconfig(self.id, fill=self.colour)

    def new_target(self, x_min=0, x_max=800, y_min=0, y_max=600):
        """ Инициализация новой цели с новыми случайными координатами, скоростями и радиусом. """
        self.r = rnd(5, 50)
        self.x = rnd(x_min + self.r, x_max - self.r)
        self.y = rnd(y_min + self.r, y_max - self.r)
        self.vx = rnd(-10, 10)
        self.vy = rnd(-10, 10)
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)

    def move(self):
        """
        Передвижение цели с постоянной скоростью, а также отражение её от стен
        """
        if self.x + self.vx > 800 - self.r:  # Условие отражения от правой стены
            self.x = 2 * (800 - self.r) - self.x - self.vx
            self.vx *= -1
        elif self.x + self.vx < self.r:  # Условие отражения от левой стены
            self.x = 2 * self.r - self.x - self.vx
            self.vx *= -1
        else:
            self.x += self.vx
        if self.y + self.vy > 600 - self.r:  # Условие отражения от пола
            self.y = 2 * (600 - self.r) - self.y - self.vy
            self.vy *= -1
        elif self.y + self.vy <self.r:  # Условие отражения от потолка
            self.y = 2 * self.r - self.y - self.vy
            self.vy *= -1
        else:
            self.y += self.vy
        # Обновление координат объекта tkinter
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )



class ball():
    def __init__(self, x=-40, y=0):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 1
        self.r = 5

        self.color = choice(['red', '#ff7f50', 'blue', 'green', '#b666d2', 'yellow', 'cyan', '#ffbf00', '#711919'])
        # Создание объекта tkinter
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        # Переменная жизни шарика, при её обнулении экзмепляр удаляется
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы ускорений self.ax, self.ay,
        и стен (от которых мяч отражается) по краям окна (размер окна 800х600).
        """
        if abs(self.vx) > 1e-1:  # условие остановки по оси х
            self.vx += self.ax
            if self.x + self.vx > 800 - self.r:  # условие отражения от правой стены
                self.x = 2 * (800 - self.r) - self.x - self.vx
                # потеря энергии от сооударений с правой стеной
                self.vy *= 0.7
                self.vx *= -0.7
            else:
                self.x += self.vx
        if abs(self.vx) > 1e-1 or self.y + self.r < 597:  # условие остановки по оси у
            self.vy += self.ay
            if self.y + self.vy > 600 - self.r:  # условие отражения от "пола"
                self.y = 2 * (600 - self.r) - self.y - self.vy
                # потеря энергии от сооударений с "полом"
                self.vy *= -0.5
                self.vx *= 0.5
            else:
                self.y += self.vy
        else:
            self.y = 600 - self.r - 3  # остановка по оси у, т. е. сохранение вертикальной координаты на уровне "пола"
        # Обновление координат объекта из tkinter
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def hittest(self, obj: target):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5 <= self.r + obj.r:  # Условие сближения центров
            # шарика и цели на расстояние, меньшее суммы их радиусов
            return True
        else:
            return False


class gun():
    def __init__(self):
        """
        Инициализация класса gun
        """
        # Коэффициент, отвечающий за модуль начальной скорости вылетающего шарика и за удлинение пушки перед выстрелом
        self.f2_power = 10
        # Переменная, показывающая, начата ли подготовка перед выстрелом или нет
        self.f2_on = 0
        # Координаты пушки в начале игры
        self.x = 50
        self.y = 570
        # Переменная скорости горизонтального движения пушки
        self.v = 5
        # Переменная угла наклона пушки к горизонтали(со знаком)
        self.an = 1
        # Длина основной части танка
        self.body_length = 40
        # Высота основной части танка
        self.body_height = 15
        # Радиус колёс танка
        self.right_wheel_rad = 6
        self.left_wheel_rad = 6
        self.right_wheel_colour = self.left_wheel_colour = choice(['red', '#ff7f50', 'blue', 'green', '#b666d2', 'yellow', 'cyan', '#ffbf00', '#711919'])
        # Переменная типа line из tkinter, отвечающая за дуло танка
        self.barrel = canv.create_line(self.x, self.y,
                                       self.x + 25 * math.cos(math.pi / 4), self.y + 25 * math.sin(math.pi / 4),
                                       width=7)
        self.body_colour = choice(['red', '#ff7f50', 'blue', 'green', '#b666d2',
                                   'yellow', 'cyan', '#ffbf00', '#711919'])
        # Переменная типа rectangle из tkinter, отвечающая за основную часть танка
        self.body = canv.create_rectangle(self.x - self.body_length / 2, self.y - 2,
                                          self.x + self.body_length / 2, self.y + self.body_height,
                                          fill=self.body_colour)
        # Переменные типа oval из tkinter, отвечающие за колёса танка
        self.right_wheel = canv.create_oval(self.x + self.body_length / 4 - self.left_wheel_rad,
                                            self.y + self.body_height,
                                            self.x + self.body_length / 4 + self.left_wheel_rad,
                                            self.y + self.body_height + 2 * self.left_wheel_rad,
                                            fill=self.left_wheel_colour)
        self.left_wheel = canv.create_oval(self.x - self.body_length / 4 - self.right_wheel_rad,
                                           self.y + self.body_height,
                                           self.x - self.body_length / 4 + self.right_wheel_rad,
                                           self.y + self.body_height + 2 * self.right_wheel_rad,
                                           fill=self.right_wheel_colour)

    def fire2_start(self, event=''):  # Начало подготовки к выстрелу, в течении которой f2_power растёт
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1  # Количество потраченных шариков
        new_ball = ball()
        new_ball.r += 5
        # Задание начальных координат нового снаряда как координат пушки в момент выстрела
        new_ball.x = self.x
        new_ball.y = self.y
        # Вычисление угла наклона пушки, зависит от положения мыши
        # +-0.3 - максимальный(и минимальный) тангенс угла наклона пушки
        if (event.x - self.x) > 0 and (event.y - self.y < -0.3 * (event.x - self.x)):
            self.an = math.atan((event.y - self.y) / (event.x - self.x))  # Нормальное вычисление угла при положении
            # мыши, удовлетворяющему ограничению (для положительного смещения по x относительно пушки)
        elif (event.x - self.x) > 0 and (event.y - self.y >= -0.3 * (event.x - self.x)):
            self.an = math.atan(-0.3)  # Предельное значение тангенса при выходе за ограничение
            # (для положительного смещения по x относительно пушки)
        elif (event.x - self.x) < 0 and (event.y - self.y < 0.3 * (event.x - self.x)):
            self.an = math.pi + math.atan((event.y - self.y) / (event.x - self.x))  # Нормальное вычисление угла при
            # положении  мыши, удовлетворяющему ограничению (для отрицательного смещения по x относительно пушки)
        elif (event.x - self.x) < 0 and (event.y - self.y >= 0.3 * (event.x - self.x)):
            self.an = math.pi + math.atan(0.3)  # Предельное значение тангенса при выходе за ограничение
            # (для отрицательного смещения по x относительно пушки)
        elif (event.x == self.x) and self.y >= event.y:
            self.an = -math.pi / 2  # задание угла для случая, когда мышь находится ровно над танком
        # Задание начальных скоростей снаряда по осям
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls += [new_ball]  # Добавление снаряда в общий массив "живых" снарядов
        self.f2_on = 0  # Окончание подготовки к выстрелу
        self.f2_power = 10  # Восстановление начальной силы выстрела

    def targetting(self, mouse_x, mouse_y):
        """Прицеливание. Зависит от положения мыши. Координаты даются функции на вход"""
        # Вычисление угла наклона пушки к вертикали, аналогично как для функции fire2_end
        if (mouse_x - self.x) > 0 and (mouse_y - self.y < -0.3 * (mouse_x - self.x)):
            self.an = math.atan((mouse_y - self.y) / (mouse_x - self.x))
        elif (mouse_x - self.x) > 0 and (mouse_y - self.y >= -0.3 * (mouse_x - self.x)):
            self.an = math.atan(-0.3)
        elif (mouse_x - self.x) < 0 and (mouse_y - self.y < 0.3 * (mouse_x - self.x)):
            self.an = math.pi + math.atan((mouse_y - self.y) / (mouse_x - self.x))
        elif (mouse_x - self.x) < 0 and (mouse_y - self.y >= 0.3 * (mouse_x - self.x)):
            self.an = math.pi + math.atan(0.3)
        elif (mouse_x == self.x) and self.y >= mouse_y:
            self.an = -math.pi / 2
        if self.f2_on:  # Рисование оранжевой пушки, если идёт подготовка к выстрелу
            canv.itemconfig(self.barrel, fill='orange')
        else:  # Рисование чёрной пушки в обратном случае
            canv.itemconfig(self.barrel, fill='black')
        # Обновление координат объекта пушки из tkinter, длина пушки зависит от f2_power
        canv.coords(self.barrel, self.x, self.y,
                    self.x + max(self.f2_power * 5 / 18 + 200 / 9, 25) * math.cos(self.an),
                    self.y + max(self.f2_power * 5 / 18 + 200 / 9, 25) * math.sin(self.an)
                    )

    def power_up(self):
        """
        Увеличение f2_power по мере подготовки к выстрелу, с ограничением сверху в 100 условных пунктов
        """
        # Смена цвета пушки в случае, если она готовится к выстрелу
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.barrel, fill='orange')
        else:
            canv.itemconfig(self.barrel, fill='black')

    def move_right(self, event=''):
        """
        Передвижение пушки вправо по горизонтали
        """
        # Условие прекращения движения, если достигнута правая граница экрана
        if self.x < 780:
            self.x += self.v
        # Обновление координат всех частей танка
        canv.coords(
            self.barrel,
            self.x,
            self.y,
            self.x + max(self.f2_power * 5 / 18 + 200 / 9, 25) * math.cos(self.an),
            self.y + max(self.f2_power * 5 / 18 + 200 / 9, 25) * math.sin(self.an)
        )
        canv.coords(
            self.body,
            self.x - self.body_length / 2,
            self.y - 2,
            self.x + self.body_length / 2,
            self.y + self.body_height,
        )
        canv.coords(
            self.left_wheel,
            self.x - self.body_length / 4 - self.right_wheel_rad,
            self.y + self.body_height,
            self.x - self.body_length / 4 + self.right_wheel_rad,
            self.y + self.body_height + 2 * self.right_wheel_rad,
        )
        canv.coords(
            self.right_wheel,
            self.x + self.body_length / 4 - self.left_wheel_rad,
            self.y + self.body_height,
            self.x + self.body_length / 4 + self.left_wheel_rad,
            self.y + self.body_height + 2 * self.left_wheel_rad,
        )

    def move_left(self, event=''):
        """
        Передвижение пушки влево по горизонтали
        """
        # Условие прекращения движения, если достигнта левая граница экрана
        if self.x > 20:
            self.x -= self.v
        # Обновление координат всех частей танка
        canv.coords(
            self.barrel,
            self.x,
            self.y,
            self.x + max(self.f2_power * 5 / 18 + 200 / 9, 25) * math.cos(self.an),
            self.y + max(self.f2_power * 5 / 18 + 200 / 9, 25) * math.sin(self.an)
        )
        canv.coords(
            self.body,
            self.x - self.body_length / 2,
            self.y - 2,
            self.x + self.body_length / 2,
            self.y + self.body_height,
        )
        canv.coords(
            self.left_wheel,
            self.x - self.body_length / 4 - self.right_wheel_rad,
            self.y + self.body_height,
            self.x - self.body_length / 4 + self.right_wheel_rad,
            self.y + self.body_height + 2 * self.right_wheel_rad,
        )
        canv.coords(
            self.right_wheel,
            self.x + self.body_length / 4 - self.left_wheel_rad,
            self.y + self.body_height,
            self.x + self.body_length / 4 + self.left_wheel_rad,
            self.y + self.body_height + 2 * self.left_wheel_rad,
        )


# Класс, собственные значения которого - последнее положение мыши при движении,

class mouse_cords():
    def __init__(self):
        self.x = 0
        self.y = 0

    def new_cords(self, event):
        """
        Функция от движения мыши, обновляет значения self.x и self.y
        """
        self.x = event.x
        self.y = event.y


# Создание двух экземпляров класса target, подклассов uniform_moving_target и lissajou_target
t1 = uniform_moving_target()
t2 = lissajou_target()
# Создание объекта из tkinter, отвечающего за вывод текста после уничтожения всех мишеней
screen1 = canv.create_text(400, 300, text='', font='28')
# Создание экземпляра класса gun
g1 = gun()
# Создание глобальных переменных, отвечающих за количество потраченных шариков и количество полученных очков
bullet = 0
points = 0
# Создание объекта из tkinter, отвечающего за вывод количества очков
id_points = canv.create_text(30, 30, text=points, font='28')
canv.itemconfig(id_points, text=points)
# Создание глобального массива с "живыми" шариками
balls = []
# Объект класса mouse_cords, хранит в себе последние координаты мыши
mc = mouse_cords()


def new_game():
    global g1, t1, screen1, balls, bullet, points, mc
    t1.new_target()
    t2.new_target()
    while ((t1.x - t2.x) ** 2 + (t1.y - t2.y) ** 2) ** 0.5 <= t1.r + t2.r:
        t2.new_target()
    bullet = 0
    balls = []
    # выстрел
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', mc.new_cords)
    # Связь нажатия стрелок на клавиатуре с движением пушки по горизонтали
    canv.bind('<d>', g1.move_right)
    canv.bind('<a>', g1.move_left)
    # Задание переменной, отвечающей за время ожидания между отрисовками последовательных кадров
    z = 1 / 60
    # Восстановление переменных жизни целей
    t1.live = 1
    t2.live = 1
    # Основной цикл игры, условие прекращения которого - отсутствующие на поле шарики и все поражённые мишени
    while t1.live or t2.live or balls:
        for b in balls:  # Действия для всех шариков из массива со всеми "живыми" шариками
            b.move()  # Передвижение шарика за одну единицу времени
            # Проверка столкновения шариков с целями, добавление очков за поражение целей,
            # обновление переменной жизни целей, а также удаление поражённых целей
            if b.hittest(t1) and t1.live:
                t1.live = 0
                points += 1
                canv.itemconfig(id_points, text=points)
                t1.hit()
            if b.hittest(t2) and t2.live:
                t2.live = 0
                points += 1
                canv.itemconfig(id_points, text=points)
                t2.hit()
            # Условие "прекращения огня" для вывода результатов уничтожения мишеней
            if not t1.live and not t2.live:
                # Привязывание кликов мыши к пустым событиям для отсутствия шариков между играми
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')
                canv.itemconfig(screen1, text='Вы уничтожили цели за ' + str(bullet) + ' выстрелов')
            if b.y == 600 - b.r - 3:  # Проверка условия остановки шарика
                b.live -= 1  # Уменьшение срока жизни шарика для последующего его удаления после остановки
            if b.live == 0:  # Удаление "мёртвых" шариков с полотна и из массива "живых" шариков
                canv.delete(b.id)
                balls.remove(b)

        # Проверка условия жизни мишени и перемещение живых мишеней
        if t1.live:
            t1.move()
        if t2.live:
            t2.move()
        canv.update()
        # Задержка между кадрами
        time.sleep(z)
        # Обновление положения дула танка за кадр
        g1.targetting(mc.x, mc.y)
        g1.power_up()
    # Стирание текста о количестве потраченных шариков перед новой игрой
    canv.itemconfig(screen1, text='')
    canv.delete(g1)
    root.after(20, new_game())  # Вызов функции new_game для старта новой игры по окончании текущей


new_game()
