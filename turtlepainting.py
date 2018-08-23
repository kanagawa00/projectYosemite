import turtle
import math

turtle.shape("turtle")
#https://docs.python.org/ja/3.7/library/turtle.html
#"arrow", "turtle", "circle", "square", "triangle", "classic"

turtle.color('red', 'yellow')
turtle.begin_fill()
while True:
    turtle.forward(200)
    turtle.left(170)
    if abs(turtle.pos()) < 1:
        break
turtle.end_fill()

def polyline(t,n,length,angle):
    for i in range(n):
        t.fd(length)
        t.lt(angle)
        
def polygon(t,n,length):
    angle=360/n
    polyline(t,n,length,angle)
#polygon(turtle,7,70,360/7)

def circle(t,r):
    circumference=2*math.pi*r
    #计算周长2Πr
    #通过画n边形画圆，n可以作为形参，也可以通过公式设定
    n=int(circumference/3)+1
    length=circumference/n
    polygon(t,n,length)

turtle.color("black", "red")
turtle.begin_fill()
circle(turtle,100)
turtle.end_fill()

def arc(t,r,angle):
    '''此处填入文档字符串'''
    length=2*math.pi*r*angle/360
    n=int(length/3)+1
    step_length=length/n
    step_angle=angle/n
    polyline(t,n,step_length,step_angle)

def circle_arc(t,r):
    arc(t,r,360)

arc(turtle,475,30)

    
turtle.done()