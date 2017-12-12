import random
from turtle import *
shape("turtle")
speed("fastest")
colors = ["blue", "purple", "cyan", "white", "yellow", "green", "orange"]
Screen().bgcolor("turquoise")
def vshape(size):
    rt(25)
    fd(size)
    bk(size)
    lt(50)
    fd(size)
    bk(size)
    rt(25)
def snowflakeArm(size):
    for x in range(0, 4):
        fd(size)
        vshape(size)
    bk(size * 4)
def snowflake(size):
    color(random.choice(colors))
    for x in range(0, 6):
        snowflakeArm(size)
        rt(60)
for i in range(0, 9):
    rt(random.randint(0,360))
    size = random.randint(5, 30)
    pensize(size / 5)
    x = random.randint(-300, 300)
    y = random.randint(-300, 300)
    penup()
    goto(x,y)
    pendown()
    snowflake(size)
