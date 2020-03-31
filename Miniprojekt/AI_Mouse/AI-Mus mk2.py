import math
from random import randint
import time
from tkinter import *

master = Tk()

#Window options
size = 800
C = Canvas(master,bg="black",height=size,width=size)
C.pack()
#Text
text =  Text(master,height=2,width=30)
text.pack()
#Grid options
w = 15
h = 15
#Other options
sizeValue = size/h
#Setup
Map = [[0 for x in range(w)] for y in range(h)]
distY = 0
distX = 0
food = 1
wall = 2
#Mouse
mouse=[math.floor(w/2),math.floor(h/2)] #Start position
energy = 10 #Start energy
speed = 0.2 #Start speed
longtermMemory = [] #Blank longterm memory
shorttermMemory = [] #Blank shortterm memory
steps = [] #Array for planned movements, in order to simulate them
#Cheese
cheese = [0,0]
cheeseLastPos = []

#Functions
def rs(inputval,sizeval):
    return inputval*sizeval
def getcoord(x,y):
    sizeValue = size/h
    x = rs(x,sizeValue)
    y = rs(y,sizeValue)
    return x,y,x+sizeValue,y+sizeValue
#Mouse moving functions
def moveMouse(steps, movingObject):
    global shorttermMemory
    global longtermMemory
    global mouse
    for move in steps:
        # if len(shorttermMemory)>10:
        #     shorttermMemory = shorttermMemory[:10]
        time.sleep(speed)
        # longtermMemory.append([mouse[0],mouse[1]])
        if move == "up" and shorttermMemory != "down":
            mouse[1] = mouse[1]-1
            C.move(movingObject,0,sizeValue)
            shorttermMemory = "up"
        elif move == "down" and shorttermMemory != "up":
            mouse[1]=mouse[1]+1
            C.move(movingObject,0,-sizeValue)
            shorttermMemory = "down"
        elif move == "left" and shorttermMemory != "right":
            mouse[0]=mouse[0]-1
            C.move(movingObject,-sizeValue,0)
            shorttermMemory = "left"
        elif move == "right" and shorttermMemory != "left":
            mouse[0]=mouse[0]+1
            C.move(movingObject,sizeValue,0)
            shorttermMemory = "right"
        print(mouse)
        C.update()
    steps.clear()
def generateStep():
    i = randint(0,3)
    if len(steps)==0:
        if i == 0:
            steps.append("up")
        elif i == 1:
            steps.append("down")
        elif i == 2:
            steps.append("left")
        elif i == 3:
            steps.append("right")
    else:
        if i == 0 and steps[-1] != "down":
            steps.append("up")
        elif i == 1 and steps[-1] != "up":
            steps.append("down")
        elif i == 2 and steps[-1] != "right":
            steps.append("left")
        elif i == 3 and steps[-1] != "left":
            steps.append("right")
def createCheese():
    global cheese
    global cheeseLastPos
    cheeseLastPos = cheese
    while cheese == cheeseLastPos:
        cheese = [randint(0,w-1),randint(0,h-1)]
    C.create_rectangle(getcoord(cheese[0],cheese[1]),fill="yellow")


#Generate Map
for row in range(0,h):
    for col in range(0,w):
        coord = distX, distY, distX+sizeValue, distY+sizeValue
        distX += sizeValue
        if Map[col][row]==1:
            C.create_rectangle(coord, fill="yellow")
        elif Map[col][row]==2:
            C.create_rectangle(coord, fill="#696969")
        elif col%2==0:
            C.create_rectangle(coord,fill="white")
        elif col%2==1:
            C.create_rectangle(coord, fill="#C0C0C0")
    distX=0
    distY+=sizeValue
#Generate mouse
Mouse = C.create_rectangle(getcoord(mouse[0],mouse[1]),fill="brown")
while energy > 0:
    generateStep()
    energy -= 1
createCheese()
moveMouse(steps, Mouse)
mainloop()
print(longtermMemory)