# -*- coding: cp1252 -*-

from winsound import PlaySound, SND_FILENAME, SND_ASYNC
from Tkinter import *
import random
import time

# canvas dimensions
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 600
# Ball radius in pixels
BALL_RADIUS = 10
# BRICKs dimensions
WIDTH_BRICK = 60
HEIGHT_BRICK = 5

#HEART dimensions
WIDTH_HEART=10
HEIGHT_HEART=10
# LIFES
LIFES = 3
POINTS=0
# delay
DELAY = 0.005
#speed components, vertical
vy = 3
#speed components, BRICKs:
vt=-3
x1=CANVAS_WIDTH/2 - BALL_RADIUS
y1=0

BRICKS=0
TRAP=None

BRICK4=None
OBJCOLLISION=None
HEART=None
touchHEART= 'C:\Windows\Media\Savanna\Windows Default.wav'
touchBRICK='C:\Windows\Media\Windows User Account Control.wav' 
BALLout= "C:\Windows\Media\Speech Sleep.wav"
lostGame= "C:\Windows\Media\Raga\Windows Critical Stop.wav"
wonGame= "C:\Windows\Media\tada.wav"
touchTRAP="C:\Windows\Media\Raga\Windows Hardware Remove.wav"

def setup():
    global BALL,TEXT1,TEXT2,TEXT3
    #Creates ball:
    BALL= canvas.create_oval(x1,y1,
                       CANVAS_WIDTH/2+BALL_RADIUS, 2*BALL_RADIUS, fill='red')
    #instructions:
    TEXT1= canvas.create_text(CANVAS_WIDTH/2 , CANVAS_HEIGHT/2 +2*BALL_RADIUS+ 20,
                                       font=('Times New Roman', 36),
                                       text = 'Clique para começar')

     #remaining lifes:
    TEXT2= canvas.create_text( 10, 10,text=  'LIFES: ' + str(LIFES), anchor=NW, font=('Times New Roman', 14),fill='blue')

     #points score:
    TEXT3 = canvas.create_text( CANVAS_WIDTH-10,10,
                             text = 'POINTS: %5d ' % (POINTS),
                             anchor=NE, font=('Times New Roman', 14),fill='maroon')


def getX(object):
    [x0, y0, x1, y1] = canvas.coords(object)
    return x1

def getY(object):
    [x0, y0, x1, y1] = canvas.coords(object)
    return y1

def beginsTurn():
    global BALL, LIFES,vy,HEART
    while 0<getY(BALL)<CANVAS_HEIGHT+2*BALL_RADIUS:
        HEART=0
        moveBALL()
        verifiesOBJCOLLISION()
        managesLandscape()
        moveBRICKS()
        if CollisionTRAP(): break
            
        if POINTS>=1000:
            gameWon()
            return

    LIFES-=1
    canvas.itemconfig(TEXT2, text = 'LIFES: ' + str(LIFES))
    playsSound(BALLout)

    
    if LIFES!=0:
        canvas.delete(BALL)
        BALL= canvas.create_oval(CANVAS_WIDTH/2 - BALL_RADIUS,0,
                   CANVAS_WIDTH/2+BALL_RADIUS,2*BALL_RADIUS , fill='red')
        vy=3
    else:
        gameOver()
    

def moveBALL():
    global POINTS,vy
    canvas.move(BALL, 0,vy)
    canvas.update() 
    time.sleep(DELAY)
    if OBJCOLLISION==None:
        POINTS+=1
    canvas.itemconfig(TEXT3, text = 'POINTS: %5d ' % (POINTS))

def createsLandscape():
    global BRICKS,BRICK1,BRICK2 ,BRICK3,BRICK4,BRICK5,HEART,x2,y2
    x2=random.uniform(0.0, CANVAS_WIDTH-WIDTH_BRICK)
    y2=CANVAS_HEIGHT
    if BRICKS==0 :
       
        BRICK1=canvas.create_rectangle(x2,y2,x2+WIDTH_BRICK,y2-HEIGHT_BRICK,
                            fill='black',tags='BRICK')
        BRICKS+=1

    if BRICKS==1 and getY(BRICK1)<CANVAS_HEIGHT-100  :
        BRICK2=canvas.create_rectangle(x2,y2,x2+WIDTH_BRICK,y2-HEIGHT_BRICK,
                            fill='black',tags='BRICK')
        BRICKS+=1

    if BRICKS==2 and getY(BRICK2)<CANVAS_HEIGHT-200:
        BRICK3=canvas.create_rectangle(x2,y2,x2+WIDTH_BRICK,y2-HEIGHT_BRICK,
                            fill='black',tags='BRICK')
        BRICKS+=1

    if BRICKS==3 and getY(BRICK3)<CANVAS_HEIGHT-100  :
        BRICK4=canvas.create_rectangle(x2,y2,x2+WIDTH_BRICK,y2-HEIGHT_BRICK,
                            fill='black',tags='BRICK')
        BRICKS+=1
        
        HEART=canvas.create_polygon(x2, y2-HEIGHT_BRICK-WIDTH_HEART,x2+WIDTH_HEART,
                                          y2-HEIGHT_BRICK-2*WIDTH_HEART,x2+2*WIDTH_HEART,
                                          y2-HEIGHT_BRICK-WIDTH_HEART,x2+WIDTH_HEART,
                                          y2-HEIGHT_BRICK,fill='magenta',
                                          outline='black',tags='BRICK') 
    if BRICKS==4 and getY(BRICK4)<CANVAS_HEIGHT-100 :
        BRICK5=canvas.create_rectangle(x2,y2,x2+WIDTH_BRICK,y2-HEIGHT_BRICK,
                            fill='black',tags='BRICK')
       
        BRICKS+=1
        
    


def moveBRICKS():
    canvas.move('BRICK',0,vt)
    canvas.update()
    time.sleep(DELAY)


def movedMouse(e):
    global x1
    if not gameOver() and not gameWon():
    
        canvas.move(BALL, e.x-BALL_RADIUS - x1 ,0 ) #horizontal ball move
        x1=e.x-BALL_RADIUS    
        if getX(BALL) <= 2*BALL_RADIUS:
            canvas.move(BALL, 2*BALL_RADIUS - getX(BALL),0)
            x1=0
        if getX(BALL)>=CANVAS_WIDTH:
            canvas.move(BALL,CANVAS_WIDTH - getX(BALL),0)
            x1=CANVAS_WIDTH-2*BALL_RADIUS

def clickedMouse(e): 
    if not gameOver() and not gameWon():
        canvas.delete(TEXT1)
        beginsTurn()



    
def verifiesOBJCOLLISION():
    global vy,vt,OBJCOLLISION
    OBJCOLLISION = detectsCollisions()
    if OBJCOLLISION != None:
        if OBJCOLLISION !=HEART and OBJCOLLISION!= TEXT3 and OBJCOLLISION!=TEXT2 and OBJCOLLISION!=TRAP:
            if getY(BALL) > getY(OBJCOLLISION)-HEIGHT_BRICK:
                dif = getY(BALL)- getY(OBJCOLLISION) + HEIGHT_BRICK
                canvas.move(BALL, 0, -dif)
            vy=vt
          
    else:
        vy=3
        
     



def detectsCollisions():
    global list,LIFES
    [xb0, yb0, xb1, yb1] = canvas.coords(BALL)
    list = canvas.find_overlapping(xb0, yb0, xb1, yb1)
    for obj in list:
        if obj ==HEART:
            playsSound(touchHEART)   
            LIFES+=1
            canvas.delete(HEART)
            canvas.itemconfig(TEXT2, text = 'LIFES: ' + str(LIFES))
    if len(list)>1:
        if list[0] != BALL  :
            return list [0]
        elif list[1] != BALL :
            return list[1]
        



def gameWon():
    if POINTS>=1000:
        canvas.delete(BALL)    
        canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2,
                                           font=('Comic Sans', 36),
                                           text = 'Congrats,',fill='pink')

        canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2+ 100,
                                           font=('Comic Sans', 36),
                                           text = 'You`re awesome!!',fill='pink')

        canvas.create_text(CANVAS_WIDTH/2,CANVAS_HEIGHT/2 +200,
                                           text = 'getting more difficult..',
                                           font=('Comic Sans', 14))
        playsSound(wonGame)
        return True


def gameOver():
    if LIFES==0:
        canvas.delete('BRICK')
        canvas.delete(BALL)
        canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2,
                                       font=('Courrier', 36),
                                       text = 'GAME OVER')
        playsSound(lostGame)
        return True

def playsSound(file):
    PlaySound(file, SND_FILENAME|SND_ASYNC)

def managesLandscape():
    global BRICK1,BRICK2,BRICK3,BRICK4,BRICK5,x2,HEART,TRAP
    x2=random.uniform(0.0, CANVAS_WIDTH-WIDTH_BRICK)
    if BRICKS<5:
            createsLandscape()
    
        
    elif BRICK1!=None and getY(BRICK1)<0:
        canvas.delete(BRICK1)
        BRICK1=canvas.create_rectangle(x2,y2,x2+WIDTH_BRICK,y2-HEIGHT_BRICK,
                        fill='black',tags='BRICK')
        
     
    elif BRICK2!=None and getY(BRICK2)<0:
        canvas.delete(BRICK2)
        BRICK2=canvas.create_rectangle(x2,y2,x2+WIDTH_BRICK,y2-HEIGHT_BRICK,
                        fill='black',tags='BRICK')
        
    elif BRICK3!=None and getY(BRICK3)<0:
        canvas.delete(BRICK3)
        
        BRICK3=canvas.create_rectangle(x2,y2,x2+WIDTH_BRICK,y2-HEIGHT_BRICK,
                        fill='black',tags='BRICK')
        if random.choice([True, False])==True:
            HEART=canvas.create_polygon(x2, y2-HEIGHT_BRICK-WIDTH_HEART,x2+WIDTH_HEART,
                                          y2-HEIGHT_BRICK-2*WIDTH_HEART,x2+2*WIDTH_HEART,
                                          y2-HEIGHT_BRICK-WIDTH_HEART,x2+WIDTH_HEART,
                                          y2-HEIGHT_BRICK,fill='magenta',
                                          outline='black',tags='BRICK')
    elif BRICK4!=None and getY(BRICK4)<0:
        canvas.delete(BRICK4)
        BRICK4=canvas.create_rectangle(x2,y2,x2+WIDTH_BRICK,y2-HEIGHT_BRICK,
                        fill='black',tags='BRICK')
   
        
    elif BRICK5!=None and getY(BRICK5)<0:
        canvas.delete(BRICK5)
        
        BRICK5=canvas.create_rectangle(x2,y2,x2+WIDTH_BRICK,y2-HEIGHT_BRICK,
                        fill='black',tags='BRICK')
        
        
        

    if BRICK4!=None and TRAP==None:
        TRAP=canvas.create_rectangle(x2,y2,x2+WIDTH_BRICK,y2-HEIGHT_BRICK,
                        fill='red',outline='magenta',tags='BRICK')
    elif TRAP!=None and getY(TRAP)<0:
            canvas.delete(TRAP)
            TRAP=canvas.create_rectangle(x2,y2,x2+WIDTH_BRICK,y2-HEIGHT_BRICK,
                        fill='red',outline='magenta',tags='BRICK')

def CollisionTRAP():
    global LIFES
    for obj in list:
        if obj ==TRAP:
            playsSound(touchTRAP)   
            return True

        

canvas = Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
background='cyan')
canvas.pack(fill=BOTH,expand=YES)

setup()

canvas.bind("<Motion>", movedMouse)
canvas.bind("<ButtonPress>", clickedMouse)

mainloop()
