from Tkinter import *
import random
import time
from math import *
import Robot

#####################################Simulation############################################

##class

robots = []
tkroot = Tk()
root = Tk()
Frame = Frame(root, width=100, height=100)
Frame.pack(expand=YES, fill=BOTH)
Frame.pack(side=TOP)
canvas = Canvas(width=1000, height=750, bg='white')
##

##one run on robots, if step() work like 20,000 time= we finsh the Simulation
def step():
   canvas.create_rectangle(300, 600,700 , 700, width=3, fill='black')
   canvas.create_rectangle(330, 330,600 , 500, width=2, fill='gray')
   epsilon_stop_simulation = 10
   epsilonRMS = 10
   send_msg()
   for r in robots:
            r.MoveRobot()
            OutFromGray()
            close_to_the_real_dist(r,epsilon_stop_simulation,epsilonRMS,r.oneStepRobot)


def run100():
    for i in range(1,100):
        step()

button1 = Button(Frame, text = "move one step only", command = step)
button2 = Button(Frame, text = "move 100 step",command=run100)


button1.pack(side=TOP)
button2.pack(side=TOP)



root.title("Ex3 GUI")
canvas.create_rectangle(300, 600,700 , 700, width=3, fill='black')
canvas.create_rectangle(330, 330,600 , 500, width=2, fill='gray')

##make random robots:
for i in range(0,100):
    random.seed(100-i)
    x=random.random()*1000
    y=random.random()*750
    while ((x>=115 and x<=215 and y>=115 and y<=215)or (x>=295 and x<=705 and y>=595 and y<=705)):
            x = random.random() * 1000
            y = random.random() * 750
    if(i<15):
          robots.insert(i,Robot.Robot(i,x,y,canvas,True,robots))##add to array
          robots[i].tempX = x
          robots[i].tempY = y
    else:
          robots.insert(i,Robot.Robot(i,x,y,canvas,False,robots))##add to array



canvas.pack(expand=YES, fill=BOTH)#Show canvas

###if Simulation Finish return true else return false
def IsSimulationFinish(robots,epsilon):
    for r in robots:
        if(r.id==64):
            continue
        if (r.isTree==False):
            return False
    return True


########################################GUI######################################
def showPosEvent(event):
    print ' X=%s Y=%s' % ( event.x, event.y)


def onMiddleClick(event):
    showPosEvent(event)

class MSG:
    def __init__(self, IDmsg, sourceMsg,  Xsender,Ysender, power ):
        self.timeMSG=time.time()
        self.IDmsg=IDmsg
        self.sourceMSG = sourceMsg
        self.Xsender=Xsender
        self.Ysender = Ysender
        self.power=power


    def updateMSG(self, power1):
        self.timeMSG=time.time()
        self.power=power1

############################## class Simulator:################################################

def swap(a, b, arr):
         t = arr[a]
         arr[a] = arr[b]
         arr[b] = t

def RandomArr(arr):
         for i in range(0, 100):
             swap(i, random.randint(0, 100), arr)

#return the oklidi dist from to point
def Get_Oklidi_Dist(x1,y1,x2,y2):
    return sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

def TreeToGuess_RealDist(Tree,Xguess,Yguess): 
    r=random.uniform(0.8, 1.2)
    return (Get_Oklidi_Dist(Tree.tempX,Tree.tempY,Xguess,Yguess)*r)


def WriteMSGtoFile(m):
    counter = 0
    file=open("RM.txt", "a")
    file.write('id_msg'+'  '+'  '+'sourceMSG'+'  '+'Xsender'+'  '+'Ysender')
    file.write('\n')
    file.write('\n')
    counter = counter+1
    file.write((str)(m.IDmsg))
    file.write('  ')
    file.write((str)(m.sourceMSG))
    file.write('  ')
    file.write((str)(m.Xsender))
    file.write('  ')
    file.write((str)(m.Ysender))
    file.write('  ')
    file.write('\n')
    file.close()

#impot: robot, Epsilon stopped the simulation, RMS Epsilon, a few pixels to move each step
# void function that upDate the guess X Y and at the end make the robot to Tree!
def close_to_the_real_dist(robot,epsilon_Stop_Simlashian,epsilonRMS,Onestep):
    Tempx=robot.tempX
    Tempy=robot.tempY
    #while we dont close to epsilon
    TempRms=RMS(Tempx,Tempy,robot.id)
    if(TempRms==0):
        return
    startRms=TempRms
    if(TempRms>RMS(Tempx,Tempy+Onestep,robot.id)and Robot.isOKtoMOVE(Tempx,Tempy+Onestep,robots)):# move up
       Tempy= Tempy + Onestep
       TempRms=RMS(Tempx,Tempy+Onestep,robot.id)
    elif (TempRms > RMS(Tempx, Tempy - Onestep,robot.id) and Robot.isOKtoMOVE(Tempx, Tempy- Onestep, robots)):  # move Down
       Tempy = Tempy - Onestep
       TempRms = RMS(Tempx, Tempy - Onestep,robot.id)
    elif (TempRms > RMS(Tempx + Onestep, Tempy,robot.id)and Robot.isOKtoMOVE(Tempx + Onestep,Tempy,robots)):  # move R
       Tempx = Tempx + Onestep
       TempRms = RMS(Tempx + Onestep, Tempy,robot.id)
    elif(TempRms>RMS(Tempx-Onestep,Tempy,robot.id)and Robot.isOKtoMOVE(Tempx - Onestep,Tempy,robots)):#movw L
       Tempx = Tempx - Onestep
       TempRms =RMS(Tempx - Onestep, Tempy,robot.id)
    else:#all is not ok! go with anathr step
       robots[robot.id].oneStepRobot=robots[robot.id].oneStepRobot+5
    robots[robot.id].tempY = Tempy
    robots[robot.id].tempX = Tempx

    #if is colse enough updata robot = make tree and tempX tempY
    if((fabs(Tempx-robots[robot.id].x)<=epsilon_Stop_Simlashian) and (fabs(Tempy-robots[robot.id].y)<=epsilon_Stop_Simlashian)and epsilonRMS>TempRms and not robot.isTree):
        i= (int)(robot.id)
        robots[i].tempY = Tempy
        robots[i].tempX = Tempx
        robots.insert(i,Robot.Robot(robot.id, robot.tempX, robot.tempY,canvas,True,robots))
        robots.remove(robot)
       
        return

def get_msg(m):
    senderRobot=m.sourceMSG
    i=robots[senderRobot-1]
    x=m.Xsender
    y=m.Ysender
    for r in robots:
        if (r.isTree== False):  #if tree- we dont insert to his array (Trese)
            dis= sqrt ((r.x-x)*(r.x-x) + (r.y-y)*(r.y-y))  #dis from the tree that send the massage
            m.updateMSG(dis)
            if (dis<=50):   #if dis less then 50- this tree get the massage
                r.Trees.append(m)
            elif (dis>50 and dis<=500):  #if dis between 50 to 500 we do a probability (histabrot)
                rand = random.random
                if (dis<=140):
                    if (rand<=1):
                        r.Trees.append(m)
                elif (dis<=230):
                    if (rand<=0.8):
                        r.Trees.append(m)
                elif (dis <= 320):
                    if (rand <= 0.6):
                        r.Trees.append(m)
                elif (dis <= 410):
                    if (rand <= 0.4):
                        r.Trees.append(m)
                elif (dis <= 500):
                    if (rand <= 0.2):
                        r.Trees.append(m)


# the STIA = if is close to zero, the geass close to the real dist
def RMS(xtemp,ytemp,idR):
    sum=0
    nemberOfTree = 0
    if (len(robots[idR].Trees)<=2):
        return 0
    for m in robots[idR].Trees:
        #if(r.isTree):
            nemberOfTree=nemberOfTree+1
            geassToTree =Get_Oklidi_Dist(m.Xsender,m.Ysender,xtemp,ytemp)
            #realDist = TreeToGuess_RealDist(r,xtemp,ytemp)
            realDist = Get_Oklidi_Dist(m.Xsender,m.Ysender,robots[idR].x,robots[idR].y)
            newDist= (realDist-geassToTree  ) * (realDist-geassToTree)
            sum = sum + newDist
    av = sum/nemberOfTree
    return sqrt(av)

def OutFromGray():  #get out from the gray area
    for i in robots:
        if ((i.x >= 330 and i.x <= 600 and i.y >= 330 and i.y <= 500) and  i.isTree==False):
            canvas.create_oval(i.x - 7, i.y - 7, i.x + 7, i.y + 7, width=0, fill='green') #delete robot
            i.y=i.y-20 #go up
            canvas.create_oval(i.x - 5, i.y - 5, i.x + 5, i.y + 5, width=0, fill='red')
            canvas.create_text(i.x,i.y)

def send_msg():
    m=0
    while (m<100):
        a=random.randint(0, 99)
        while(robots[a].isTree==False):
            a = random.randint(0, 99)
        r= robots[a]

        msg= MSG( (r.id*1000)+r.counterMSG, r.id, r.x, r.y, 0)
        r.counterMSG=r.counterMSG+1
        WriteMSGtoFile(msg)
        get_msg(msg)
        m=m+1



canvas.bind('<Button-1>',  onMiddleClick)
canvas.pack(expand=YES, fill=BOTH)
Frame.pack(expand=YES, fill=BOTH)
tkroot.title('Ex3')
tkroot.mainloop()
