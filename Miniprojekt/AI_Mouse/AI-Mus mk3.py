import math
from random import randint
import time
from tkinter import *
# Generate base window
master = Tk()
size = 600
# Canvas
C = Canvas(master, bg='black', height=size, width=size)
C.pack()
# Text
text = Text(master, height=2, width=30)
text.pack()

# Define classes


class World:
    def __init__(self, tile):
        self.tile = tile
        self.weight = 100
        self.bounds = None
        self.tile_object = None

    def updValue(self):
        # C.itemconfigure(self.tile_object, fill=_from_rgb((self.weight, 0, 0)))
        C.update()


class humanObject:
    def __init__(self, tile, color, speed, energy):
        self.tile = tile
        self.color = color
        self.speed = speed
        self.energy = energy
        self.soul = None
        self.steps = 0
        self.tile_id = sideLength*self.tile[1]-(sideLength-self.tile[0])

    def create(self):
        self.soul = C.create_rectangle(
            getcoord(self.tile[0]-1, self.tile[1]-1), fill=self.color)
        C.update()

    def move(self):
        move = []
        weight = []
        tiles = []
        selected = None
        movable = [[self.tile[0]+1, self.tile[1]], [self.tile[0]-1, self.tile[1]],
                   [self.tile[0], self.tile[1]+1], [self.tile[0], self.tile[1]-1]]
        for item in movable:
            ID = item[1]*sideLength-(sideLength-item[0])-1
            #Sortera bort rutor utanför spelplanen
            if item[0] < 1 or item[0] > sideLength or item[1] < 1 or item[1] > sideLength:
                movable.remove(item)
            elif (ID == len(WorldArray)):
                movable.remove(item)
        for item in movable:
            ID = item[1]*sideLength-(sideLength-item[0])-1
            move.append([item[0]-self.tile[0], item[1]-self.tile[1]])
            try:
                weight.append(WorldArray[ID].weight)
                tiles.append(WorldArray[ID])
            except:
                None
        weight.sort()
        tiles1 = []
        j = randint(0,len(tiles)-1)
        for i in range(len(tiles)):
            tiles1.append(tiles[j])
            j += 1
            if j > len(tiles)-1:
                j = 0
        #Välj "bästa" rutan
        for tile in tiles1:
            if tile.weight == weight[0]:
                selected = tile

        if selected.tile[0] > self.tile[0]:
            moveX = sizeValue
        elif selected.tile[0] < self.tile[0]:
            moveX = -sizeValue
        else:
            moveX = 0

        if selected.tile[1] > self.tile[1]:
            moveY = sizeValue
        elif selected.tile[1] < self.tile[1]:
            moveY = -sizeValue
        else:
            moveY = 0
        C.move(self.soul, moveX, moveY)
        ID = self.tile[1]*sideLength-(sideLength-self.tile[0])-1
        WorldArray[ID].weight = 255
        walked.append(WorldArray[ID])
        self.tile = selected.tile
        WorldArray[ID].updValue()
        self.steps += 1
        # print(self.steps)
        if self.steps == 10:
            for cheese in food:
                cheese.area += 1
                cheese.smell()
            self.steps = 0
        C.update()
    
    def checkHit(self):
        for cheese in food:
            if self.tile == cheese.tile:
                print('HIT')
                ID = (cheese.tile[1]-1)*sideLength+(cheese.tile[0]-1)
                WorldArray[ID].weight = 255
                WorldArray[ID].updValue()
                C.delete(cheese.tile_object)
                for item in cheese.effect:
                    ID = (item[1]-1)*sideLength+item[0]-1
                    WorldArray[ID].weight = 100
                    WorldArray[ID].updValue()
                food.remove(cheese)
                makeCheese()
                for item in walked:
                    item.weight = 100
                    item.updValue()
                walked.clear()
                self.energy = 50 

def makeCheese():
    food.append(cheese())

class cheese:
    def __init__(self):
        self.tile = WorldArray[randint(1,len(WorldArray)-1)].tile
        # self.tile = [11,11]
        self.area = 0
        self.tile_object = C.create_rectangle(getcoord(self.tile[0]-1,self.tile[1]-1),fill="#ffa600")
        self.effect = []
        ID = (self.tile[1]-1)*sideLength + self.tile[0]-1
        WorldArray[ID].weight = -100
    def smell(self):
        for i in range(self.area):
            if (self.tile[0]+(i+1)>sideLength):
                None
            else:
                self.effect.append([self.tile[0]+(i+1),self.tile[1]])
                #Ränkar ut vikterna
                ID = (self.tile[1]-1)*sideLength+self.tile[0]+(i+1)-1
                WorldArray[ID].weight = math.floor(100*(i/sideLength))
                WorldArray[ID].updValue()
            #
            if (self.tile[0]-(i+1)<1):
                None
            else:
                self.effect.append([self.tile[0]-(i+1),self.tile[1]])
                ID = (self.tile[1]-1)*sideLength+self.tile[0]-(i+1)-1
                WorldArray[ID].weight = math.floor(100*(i/sideLength))
                WorldArray[ID].updValue()
            #
            if (self.tile[1]+(i+1)>sideLength):
                None
            else:
                self.effect.append([self.tile[0],self.tile[1]+(i+1)])
                ID = (self.tile[1]+(i+1)-1)*sideLength+self.tile[0]-1
                WorldArray[ID].weight = math.floor(100*(i/sideLength))
                WorldArray[ID].updValue()
            #
            if (self.tile[1]-(i+1)<1):
                None
            else:
                self.effect.append([self.tile[0],self.tile[1]-(i+1)])
                ID = (self.tile[1]-(i+1)-1)*sideLength+self.tile[0]-1
                WorldArray[ID].weight = math.floor(100*(i/sideLength))
                WorldArray[ID].updValue()
            if i == self.area-1:
                for j in range(i+1):
                    for k in range((i-j)):
                        #Resten av diamanten dvs de fyra trianglarna
                        if self.tile[0]+(j+1)>sideLength or self.tile[1]-(k+1)<1:
                            None
                        else:
                            self.effect.append([self.tile[0]+(j+1),self.tile[1]-(k+1)])
                            #Ränkar ut vikterna
                            ID = (self.tile[1]-(k+1)-1)*sideLength+self.tile[0]+(j+1)-1
                            WorldArray[ID].weight = math.floor((10*(k*(i/sideLength)+j*(i/sideLength)))*(i/sideLength))
                            WorldArray[ID].updValue()
                        #
                        if self.tile[0]-(j+1)<1 or self.tile[1]-(k+1)<1:
                            None
                        else:
                            self.effect.append([self.tile[0]-(j+1),self.tile[1]-(k+1)])
                            ID = (self.tile[1]-(k+1)-1)*sideLength+self.tile[0]-(j+1)-1
                            WorldArray[ID].weight = math.floor((10*(k*(i/sideLength)+j*(i/sideLength)))*(i/sideLength))
                            WorldArray[ID].updValue()
                        #
                        if self.tile[0]+(j+1)>sideLength or self.tile[1]+(k+1)>sideLength:
                            None
                        else:
                            self.effect.append([self.tile[0]+(j+1),self.tile[1]+(k+1)])
                            ID = (self.tile[1]+(k+1)-1)*sideLength+self.tile[0]+(j+1)-1
                            WorldArray[ID].weight = math.floor((10*(k*(i/sideLength)+j*(i/sideLength)))*(i/sideLength))
                            WorldArray[ID].updValue()
                        #
                        if self.tile[0]-(j+1)<1 or self.tile[1]+(k+1)>sideLength:
                            None
                        else:
                            self.effect.append([self.tile[0]-(j+1),self.tile[1]+(k+1)])
                            ID = (self.tile[1]+(k+1)-1)*sideLength+self.tile[0]-(j+1)-1
                            WorldArray[ID].weight = math.floor((10*(k*(i/sideLength)+j*(i/sideLength)))*(i/sideLength))
                            WorldArray[ID].updValue()
        for item in self.effect:
            if item[0] < 1 or item[0] > sideLength or item[1] < 1 or item[1] > sideLength:
                self.effect.remove(item)
        IDs = []
        for item in self.effect:
            ID = (item[1]-1)*sideLength+item[0]-1
            IDs.append(ID)
            # WorldArray[ID].weight = 1
            try:
                WorldArray[ID].updValue()
            except:
                None
            C.update()

def updWalkedTiles():
    for item in walked:
        item.weight = math.floor(item.weight * 0.99)
        if item.weight < 100:
            item.weight = 101
            walked.remove(item)
        item.updValue()

# Generate blueprint map
walked = []
sideLength = 15
Map = [[0 for x in range(sideLength)] for y in range(sideLength)]
WorldArray = []
distY = 0
distX = 0
sizeValue = size/sideLength
current_map = []
smellrange = 5
cheese_amount = 1
player_amount = 1


def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb
# Define functions
def rs(inputval, sizeval):
    return inputval*sizeval


def getcoord(x, y):
    sizeValue = size/sideLength
    x = rs(x, sizeValue)
    y = rs(y, sizeValue)
    return x, y, x+sizeValue, y+sizeValue


def updMapValues():
    for item in WorldArray:
        item.updValue()


# Generate actual map array
for i in range(len(Map)):
    for j in range(len(Map[i])):
        WorldArray.append(World([j+1, i+1]))
        coord = distX, distY, distX+sizeValue, distY+sizeValue
        distX += sizeValue
        WorldArray[len(WorldArray)-1].tile_object = C.create_rectangle(coord,
        fill=_from_rgb((WorldArray[len(WorldArray)-1].weight, 0, 0)))
        WorldArray[len(WorldArray)-1].bounds = coord
    distX = 0
    distY += sizeValue
# player = humanObject([1,sideLength], "blue", 2.0, 50)


food = []
player = []

for i in range(cheese_amount):
    food.append(cheese())
    food[len(food)-1].smell()
for i in range(player_amount):
    player.append(humanObject([randint(1,sideLength),randint(1,sideLength)],"blue",0.1,50))
    player[len(player)-1].create()

for i in WorldArray:
    try:
        i.updValue()
    except: 
        None

while True:
    for play in player:
        # print(play.energy)
        # if play.energy > 0:
        #     time.sleep(play.speed)
        #     play.move()
        #     play.checkHit()
        #     updWalkedTiles()
        #     play.energy -= 1
        # else:
        #     C.delete(play.soul)
        #     player.remove(play)
        time.sleep(play.speed)
        play.move()
        play.checkHit()
        updWalkedTiles()
    if len(player) == 0:
        break


# for item in WorldArray:
#     print(item.__dict__)

mainloop()
