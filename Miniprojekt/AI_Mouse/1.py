from tkinter import *

master = Tk()
size = 600
C = Canvas(master, bg="white",height=size,width=size)
C.pack()

class test:
    def __init__(self):
        self.item = None
objArray = []
objArray.append(test())
objArray.append(test())
print(objArray)

objArray[0].item = C.create_rectangle((size/2)-100,(size/2)-100,(size/2)+100,(size/2)+100, fill="blue")
objArray[1].item = C.create_rectangle(0,0,100,100, fill="blue")
for i in range(len(objArray)):
    C.itemconfigure(objArray[i].item, fill="red")
for item in objArray:
    C.itemconfigure(item.item,fill="green")
mainloop()