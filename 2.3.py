import turtle

turtle.penup()
turtle.goto(-300,0)
x=-300
y=0
vx=10
vy=40
ay=-10
dt=0.01
c=0.9
turtle.pendown()
turtle.shape('turtle')
turtle.tracer(2)
for i in range(int(100/dt)):
    turtle.goto(x,y)
    x+=vx*dt
    y+=vy*dt + ay*dt**2/2
    vy+=ay*dt
    if (y<=0 and vy<=0):
        vy=-vy*c
