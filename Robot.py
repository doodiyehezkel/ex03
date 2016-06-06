from Tkinter import *
import random
import time
from math import *
def isOKtoMOVE(tempX, tempY,robots):
    if (tempX > 1000 or tempX < 0):  # if its not in the limit of the canvas
            return False

    if (tempY > 750 or tempY < 0):
            return False
    elif ((tempX >= 115 and tempX <= 215 and tempY >= 115 and tempY <= 215) or (
                                tempX >= 295 and tempX <= 705 and tempY >= 595 and tempY <= 705)):  # if its in a black area
            return False
    for i in robots:
         if (i.x-5<tempX and i.x+5>tempX and i.y-5<tempY and i.y+5>tempY):
            return False
    else:
            return True
class Robot:
    x = 0
    y = 0
    id = 0
    battery = 70
    IsWhite = None
    tempX=250
    tempY=250
    counterMSG=0
    disForTree= None
    canvas = None
    robots=[]
    Trees = [] # the tree that received MSG copy by pointer here!
    oneStepRobot=5
    def __init__(self, id, x, y,canvas,isTree,robots):
        start_time = time.time()
        self.id = id
        self.x = x
        self.y = y
        self.isTree=isTree
        start_time = time.time()
        self.history_path = []
        self.env = []
        self.canvas=canvas
        self.robots=robots
        self.oneStepRobot=5
        self.Trees=[]
        if(isTree):
             canvas.create_oval(x - 3, y - 3, x + 3, y + 3, width=0,fill='red')
             canvas.create_text(x, y)
        else:
             canvas.create_oval(x - 3, y - 3, x + 3, y + 3, width=0,fill='green')
             canvas.create_text(x, y)


        if ((x >= 330 and x <= 600 and y >= 330 and y <= 500)):
            self.IsWhite = False
        else:
            self.IsWhite = True

    def control_battery(self):
        if (self.IsWhite and self.battery < 100):
            self.battery = self.battery + 1
        elif ((not self.IsWhite) and self.battery > 0):
            self.battery = self.battery - 1

    def MoveRobot(self):
        if (self.isTree):
            self.canvas.create_oval(self.x - 3, self.y - 3, self.x + 3, self.y + 3, width=0, fill='red')
            self.canvas.create_text(self.x, self.y)
            return

        if (self.x >= 330 and self.x <= 600 and self.y >= 330 and self.y <= 500):  # delete the old robot
            self.canvas.create_oval(self.x - 7, self.y - 7, self.x + 7, self.y + 7, width=0, fill='green')
        else:
            self.canvas.create_oval(self.x - 7, self.y - 7, self.x + 7, self.y + 7, width=0, fill='white')

        # find a new x, y for the robot
        while (True):
            MoveTo = random.random()
            if (MoveTo < 0.25):  # move right
                tempX = self.x + 5
                tempY = self.y
            elif (MoveTo < 0.50):  # move left
                tempX = self.x - 5
                tempY = self.y
            elif (MoveTo < 0.75):  # move up
                tempY = self.y + 5
                tempX = self.x
            else:                # move down
                tempY = self.y - 5
                tempX = self.x

            if (isOKtoMOVE(tempX,tempY,self.robots)):  # if the point is in good area- break while
                self.x = tempX
                self.y = tempY
                break

        self.canvas.create_oval(self.x - 5, self.y - 5, self.x + 5, self.y + 5, width=0,fill='green')  # create a robot in the new x,y
        self.canvas.create_text(self.x,self.y)

        self.control_battery



    def addPath(self,s):
        self.history_path[self.history_path.size]=s
