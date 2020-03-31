import math
import random
import time
from tkinter import *


master = Tk()

size=400

C = Canvas(master, bg='black', height=size, width=size)
C.pack()

text = Text(master,height=2,width=30)
text.pack()
# text.insert(END, "Testtext \növer två rader\n")

w = 12
h = 12
distY = 0
distX = 0
sizeValue = size/h
n_walls = 0
Map = [[0 for x in range(w)] for y in range(h)]
food = 1
wall = 2

#Ost
cheeseeatten = 0
n_food = 1
cheeseamount = 10
currentcheeses = 0
cheeseplaces=[[3,3],[2,1],[4,5],[7,3],[2,8],[9,1],[5,7],[8,3],[4,1],[2,7],[5,4]]
speed = 0.2

#Skapa Musen
#musdetaljer
korttidsminne=[]
långtidsminne=[]
energi=50
mouse=[1,2] #position

def createCheese():
    global currentcheeses
    if cheeseamount>currentcheeses:
        ptpc = random.randint(0,len(cheeseplaces)-1)
        x = cheeseplaces[ptpc][0]
        y = cheeseplaces[ptpc][1]
        C.create_rectangle(getcoord(x,y),fill="yellow")
        currentcheeses+=1
        global Map
        Map[x][y]=1

def rs(inputval,sizeval):
    return inputval*sizeval
def getcoord(x,y):
    sizeValue = size/h
    x = rs(x,sizeValue)
    y = rs(y,sizeValue)
    return x,y,x+sizeValue,y+sizeValue
def MoveMouse(mouse1,movingObject):
    time.sleep(speed)
    global mouse
    if mouse[0]<=-1:
        mouse1[0]=1
        mouse[0]=mouse[0]+2
    elif mouse[1]<=-1:
        mouse1[1]=1
        mouse[0]=mouse[0]+2
    elif mouse[0]>=w:
        mouse1[0]=-1
        mouse[0]=mouse[0]-2
    elif mouse[1]>=h:
        mouse1[1]=-1
        mouse[1]=mouse[1]-2
    dx=mouse1[0]*sizeValue
    dy=mouse1[1]*sizeValue
    C.move(movingObject,dx,dy)
    createCheese()
    C.update()

def FoundChese(mousepos):
    global Map
    if Map[mousepos[0]][mousepos[1]]==1:
        outputtext="Found Cheese at"+str(mouse[0])+" X "+str(mouse[1])+" Y/nAdded to longterm memory"
        global cheeseeatten
        cheeseeatten+=1
        text.insert(INSERT,outputtext)
        global långtidsminne
        långtidsminne.append([mousepos[0],mousepos[1]])
        C.create_rectangle(getcoord(mousepos[0],mousepos[1]), fill="orange")
        Map[mousepos[0]][mousepos[1]]=0
        global energi 
        energi += 10
        global currentcheeses
        currentcheeses-=1

def MovePlanner(steps):
    whattodo = random.randint(0,3)
    if whattodo==0:
        print("kortis")
        korttidsminne= Lookinlongterm(steps)
    elif whattodo==1:
        print("långis")
        korttidsminne = Lookinshortterm(steps)
    else:
        print("random")
        korttidsminne=Wanderrandom(steps)
    print(korttidsminne)
    return korttidsminne

def Wanderrandom(steps):
    steglista=[]
    formerstep=5
    while steps>0:
        samma = False
        typavsteg = random.randint(0,3)
        if typavsteg==0 and formerstep!=1:
            steglista.append("upp")
        elif typavsteg==1 and formerstep!=0:
            steglista.append("ner")
        elif typavsteg==2 and formerstep!=3:
            steglista.append("vänster")
        elif typavsteg==3 and formerstep!=2:
            steglista.append("höger")
        else:
            samma=True
        if samma==False:
            formerstep = typavsteg
            steps-=1
    return steglista

def Lookinlongterm(steps):
    if len(långtidsminne)==0:
        return Wanderrandom(steps)
    else:
        Memoryplace = random.randint(0,len(långtidsminne)-1)
        Minnet = långtidsminne[Memoryplace]
        målX = Minnet[0]-mouse[0]
        målY = Minnet[1]-mouse[1]
        steglista = []
        while steps>0:
            if målX<0:
                steglista.append('upp')
                målX+=1
            elif målX>0:
                steglista.append('ner')
                målX-=1
            elif målY<0:
                steglista.append('vänster')
                målY+=1
            elif målY>0:
                steglista.append('höger')
                målY-=1
            else:
                steglista.append(Wanderrandom(1)[0])
            steps-=1
def Lookinshortterm(steps):
    if len(korttidsminne)==0:
        return Wanderrandom(steps)
    else:
        meströrelse=[0,0,0,0]
        for minnen in korttidsminne:
            if minnen=="upp":
                meströrelse[0]+=1
            elif minnen=="ner":
                meströrelse[1]+=1
            elif minnen=="vänster":
                meströrelse[2]+=1
            elif minnen=="höger":
                meströrelse[3]+=1
        Lodrätt=""
        Vågrätt=""
        if meströrelse[0]>meströrelse[1]:
            Lodrätt = "upp"
        else:
            Lodrätt = "ner"
        if meströrelse[2]>meströrelse[3]:
            Vågrätt="vänster"
        else:
            Vågrätt="höger"
        steglista=[]
        while steps > 0:
            if steps%2==0:
                steglista.append(Lodrätt)
            else:
                steglista.append(Vågrätt)
            steps-=1
        return steglista

for i in range(n_walls):
    pHeight = random.randint(0,h-1)
    pWidth = random.randint(0,w-1)
    Map[pHeight][pWidth] = wall
# for i in range(n_food):
#     pHeight = random.randint(0,h-1)
#     pWidth = random.randint(0,w-1)
#     Map[pHeight][pWidth] = food

for row in range(0,h):
    for col in range(0,w):
        coord = distX, distY, distX+sizeValue,distY+sizeValue
        distX += sizeValue
        if Map[col][row]==1:
            C.create_rectangle(coord, fill="yellow")
        elif Map[col][row]==2:
            C.create_rectangle(coord,fill="#696969")
        elif col%2==0:
            C.create_rectangle(coord,fill="white")
        elif col%2==1:
            C.create_rectangle(coord, fill="#C0C0C0")
    distY+=sizeValue
    distX=0

# mouse = [5,5]
Mouse = C.create_rectangle(getcoord(mouse[0],mouse[1]),fill="brown")

mousemove = MovePlanner(random.randint(3,10))

while energi>0:
    energiförbrukning = random.randint(1,10)
    mousemove=MovePlanner(energiförbrukning)
    energi-=energiförbrukning
    while len(mousemove)>0:
        steg=[0,0]
        C.create_rectangle(getcoord(mouse[0],mouse[1]),fill="blue")
        if mousemove[0]=="upp":
            mouse[1] = mouse[1]-1
            steg[1] -=1
        elif mousemove[0]=="ner":
            mouse[1]=mouse[1]+1
            steg[1]+=1
        elif mousemove[0]=="vänster":
            mouse[0]=mouse[0]-1
            steg[0]-=1
        elif mousemove[0]=="höger":
            mouse[0]=mouse[0]+1
            steg[0]+=1
        MoveMouse(steg,Mouse)
        FoundChese(mouse)
        mousemove.pop(0)
    text.delete("insert linestart", "insert lineend")
    text.insert(END, str(energiförbrukning)+ " steps taken, "+str(energi)+" energy left!")
text.delete("insert linestart", "insert lineend")
text.insert(END, "Out of steps!\nCheese eaten "+str(cheeseeatten))
    

#print map
# for i in Map:
#     print(i)
mainloop()