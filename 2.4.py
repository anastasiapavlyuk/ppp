import turtle
from random import randint, randrange

a=300
turtle.tracer(False)
turtle.penup()
turtle.goto(a, a)
turtle.pendown()
turtle.goto(a, -a)
turtle.goto(-a, -a)
turtle.goto(-a, a)
turtle.goto(a, a)

turtle.tracer(True)

number_of_turtles = 150
steps_of_time_number = 100000

turtle.tracer(False)

pool = [turtle.Turtle(shape='turtle') for i in range(number_of_turtles)]
for unit in pool:
    unit.penup()
    unit.speed(10)
    unit.goto(randint(-200, 200), randint(-200, 200))
    unit.left(randint(0,360))
    unit.shape("circle")

turtle.tracer(True)

turtle.tracer(200)
v=0
for i in range(steps_of_time_number):
    for unit in pool:
        v=5
        y=unit.ycor()
        x=unit.xcor()
        if (x>-a+v and x<a-v and y>-a+v and y<a-v):
            unit.forward(v)
        else:
            unit.left(90)
            unit.forward(v)
