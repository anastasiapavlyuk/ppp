import turtle
from random import *

turtle.shape('turtle')

for i in range(20):
    turtle.forward(randint(1,50))
    turtle.left(randint(0,360))