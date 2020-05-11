import math
from random import randint
import time
from tkinter import *
# Generate tkinter window
master = Tk()
size = 600  # Change window size (does not effect amout of tiles)
# Canvas
C = Canvas(master, bg='black', height=size, width=size)
C.pack()
# Text
# text = Text(master, height=2, width=30)
# text.pack()
debug = False  # Boolean
food = []
player = []

def debugToggle():
    global debug
    if debug:
        debug = False
        for i in range(sideLength):
            for j in range(sideLength):
                if j%2 == 0:
                    color_value = "#254b00"
                elif j%2 == 1:
                    color_value = "#567D46"
                ID = (i*sideLength)+j
                C.itemconfigure(WorldArray[ID].tile_object, fill=color_value)
                

    else:
        debug = True
        for item in WorldArray:
            item.updValue()
    print(debug)

def addPlayer():
    player.append(humanObject(
        [randint(1, sideLength), randint(1, sideLength)], "blue", 0.1, 50))
    player[len(player)-1].create()
    btn_text.set("Add player ["+str(len(player))+"]")

def addFood():
    makeCheese()
    btn_text1.set("Add food ["+str(len(food))+"]")

btn_text = StringVar()
btn_text1 = StringVar()
btn_text1.set("Add food ["+str(len(food)+1)+"]")
btn_text.set("Add player ["+str(len(player)+1)+"]")
b = Button(master, text="Debug (on/off)", command=debugToggle)
b1 = Button(master, textvariable=btn_text, command=addPlayer)
b2 = Button(master, textvariable=btn_text1, command=addFood)
b.pack()
b1.pack()
b2.pack()


# Define classes

# World map, in charge of generating and displaying simulation.
class World:
    def __init__(self, tile):
        self.tile = tile
        self.weight = 100
        self.bounds = None
        self.tile_object = None

    def updValue(self):
        self.weight += 1
        if debug:
            try:
                # Uncomment for visual weight map for debugging.
                C.itemconfigure(self.tile_object, fill=_from_rgb((self.weight, 0, 0)))
            except:
                None
        C.update()

# The "mouse" character, in charge of itself and communicating to the world for senses.


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
        # Reset array values.
        move = []
        weight = []
        tiles = []
        selected = None
        # Add all nerby tiles to an array.
        movable = [[self.tile[0]+1, self.tile[1]], [self.tile[0]-1, self.tile[1]],
                   [self.tile[0], self.tile[1]+1], [self.tile[0], self.tile[1]-1]]
        for item in movable:
            ID = item[1]*sideLength-(sideLength-item[0])-1
            # Remove tiles outside of playing field for the array.
            if item[0] < 1 or item[0] > sideLength or item[1] < 1 or item[1] > sideLength:
                movable.remove(item)
            elif (ID == len(WorldArray)):
                movable.remove(item)
        for item in movable:
            # Get world ID for each tile for later communication to world object.
            ID = item[1]*sideLength-(sideLength-item[0])-1
            move.append([item[0]-self.tile[0], item[1]-self.tile[1]])
            try:
                weight.append(WorldArray[ID].weight)
                tiles.append(WorldArray[ID])
            except:
                None
        # Sort tiles by "weight" to determine most profitable next step (ei prevent going backwards and more)
        weight.sort()
        tiles1 = []  # New array reset
        j = randint(0, len(tiles)-1)
        for i in range(len(tiles)):
            tiles1.append(tiles[j])
            j += 1
            if j > len(tiles)-1:
                j = 0
        # Pick "best" square
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
        C.move(self.soul, moveX, moveY)  # Move the actual player
        ID = self.tile[1]*sideLength-(sideLength-self.tile[0])-1
        # Change the weigt of previous square to avoid backtracking.
        WorldArray[ID].weight = 255
        # Add to array or recently walked tiles to better prevent stepping of same tiles twice within a limited range.
        walked.append(WorldArray[ID])
        self.tile = selected.tile
        WorldArray[ID].updValue()
        self.steps += 1
        # print(self.steps)
        # Every 10 steps (player steps) update the cheese for a gradual effect increase.
        if self.steps == 10:
            for cheese in food:
                cheese.area += 1
                cheese.smell()
            self.steps = 0
        C.update()

    def checkHit(self):  # Check if on the same tile as cheese.
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
                makeCheese()  # Generate new cheese.
                for item in walked:
                    item.weight = 100
                    item.updValue()
                walked.clear()
                self.energy = 50


def makeCheese():
    food.append(cheese())


class cheese:  # Class for food object, in charge of holding all food attributes and knowledge of the food position.
    def __init__(self):
        self.tile = WorldArray[randint(1, len(WorldArray)-1)].tile
        self.area = 0
        self.tile_object = C.create_rectangle(
            getcoord(self.tile[0]-1, self.tile[1]-1), fill="#ffa600")
        self.effect = []
        ID = (self.tile[1]-1)*sideLength + self.tile[0]-1
        WorldArray[ID].weight = -100

    def smell(self):
        for i in range(self.area):
            if (self.tile[0]+(i+1) > sideLength):
                None
            else:
                self.effect.append([self.tile[0]+(i+1), self.tile[1]])
                # Calculate weights and update corresponding world tile object.
                ID = (self.tile[1]-1)*sideLength+self.tile[0]+(i+1)-1
                WorldArray[ID].weight = math.floor(100*(i/sideLength))
                WorldArray[ID].updValue()
            #
            if (self.tile[0]-(i+1) < 1):
                None
            else:
                self.effect.append([self.tile[0]-(i+1), self.tile[1]])
                ID = (self.tile[1]-1)*sideLength+self.tile[0]-(i+1)-1
                WorldArray[ID].weight = math.floor(100*(i/sideLength))
                WorldArray[ID].updValue()
            #
            if (self.tile[1]+(i+1) > sideLength):
                None
            else:
                self.effect.append([self.tile[0], self.tile[1]+(i+1)])
                ID = (self.tile[1]+(i+1)-1)*sideLength+self.tile[0]-1
                WorldArray[ID].weight = math.floor(100*(i/sideLength))
                WorldArray[ID].updValue()
            #
            if (self.tile[1]-(i+1) < 1):
                None
            else:
                self.effect.append([self.tile[0], self.tile[1]-(i+1)])
                ID = (self.tile[1]-(i+1)-1)*sideLength+self.tile[0]-1
                WorldArray[ID].weight = math.floor(100*(i/sideLength))
                WorldArray[ID].updValue()
            if i == self.area-1:
                for j in range(i+1):
                    for k in range((i-j)):
                        # Resten av diamanten dvs de fyra trianglarna
                        if self.tile[0]+(j+1) > sideLength or self.tile[1]-(k+1) < 1:
                            None
                        else:
                            self.effect.append(
                                [self.tile[0]+(j+1), self.tile[1]-(k+1)])
                            # Ränkar ut vikterna
                            ID = (self.tile[1]-(k+1)-1) * \
                                sideLength+self.tile[0]+(j+1)-1
                            WorldArray[ID].weight = math.floor(
                                (10*(k*(i/sideLength)+j*(i/sideLength)))*(i/sideLength))
                            WorldArray[ID].updValue()
                        #
                        if self.tile[0]-(j+1) < 1 or self.tile[1]-(k+1) < 1:
                            None
                        else:
                            self.effect.append(
                                [self.tile[0]-(j+1), self.tile[1]-(k+1)])
                            ID = (self.tile[1]-(k+1)-1) * \
                                sideLength+self.tile[0]-(j+1)-1
                            WorldArray[ID].weight = math.floor(
                                (10*(k*(i/sideLength)+j*(i/sideLength)))*(i/sideLength))
                            WorldArray[ID].updValue()
                        #
                        if self.tile[0]+(j+1) > sideLength or self.tile[1]+(k+1) > sideLength:
                            None
                        else:
                            self.effect.append(
                                [self.tile[0]+(j+1), self.tile[1]+(k+1)])
                            ID = (self.tile[1]+(k+1)-1) * \
                                sideLength+self.tile[0]+(j+1)-1
                            WorldArray[ID].weight = math.floor(
                                (10*(k*(i/sideLength)+j*(i/sideLength)))*(i/sideLength))
                            WorldArray[ID].updValue()
                        #
                        if self.tile[0]-(j+1) < 1 or self.tile[1]+(k+1) > sideLength:
                            None
                        else:
                            self.effect.append(
                                [self.tile[0]-(j+1), self.tile[1]+(k+1)])
                            ID = (self.tile[1]+(k+1)-1) * \
                                sideLength+self.tile[0]-(j+1)-1
                            WorldArray[ID].weight = math.floor(
                                (10*(k*(i/sideLength)+j*(i/sideLength)))*(i/sideLength))
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


# Array of recently walked tiles to prevent backtracking and non-benefical movement.
def updWalkedTiles():
    for item in walked:
        item.weight = math.floor(item.weight * 0.99)
        if item.weight < 100:
            item.weight = 101
            walked.remove(item)
        item.updValue()


# Generate blueprint map
walked = []

sideLength = 15  # Change to increase/decrease map size.

Map = [[0 for x in range(sideLength)] for y in range(sideLength)]
WorldArray = []
distY = 0
distX = 0
sizeValue = size/sideLength
current_map = []

cheese_amount = 1  # Change to increase/decrease amout of cheese
player_amount = 1  # Change to increase/decrease amout of players


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
        if j % 2 == 0:
            color_value = "#254b00"
        else:
            color_value = "#567D46"
        WorldArray.append(World([j+1, i+1]))
        coord = distX, distY, distX+sizeValue, distY+sizeValue
        distX += sizeValue
        ID = len(WorldArray)-1
        # color_value = _from_rgb((WorldArray[len(WorldArray)-1].weight, 0, 0))
        WorldArray[len(WorldArray)-1].tile_object = C.create_rectangle(coord,
                                                                       fill=color_value)
        WorldArray[len(WorldArray)-1].bounds = coord
    distX = 0
    distY += sizeValue




for i in range(cheese_amount):
    food.append(cheese())
    food[len(food)-1].smell()
for i in range(player_amount):
    player.append(humanObject(
        [randint(1, sideLength), randint(1, sideLength)], "blue", 0.1, 50))
    player[len(player)-1].create()

for i in WorldArray:
    try:
        i.updValue()
    except:
        None

while True:
    # Uncomment for survival aspect (best with multiple players)
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

mainloop()
