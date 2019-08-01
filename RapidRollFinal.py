# -*- coding: cp1252 -*-

from winsound import PlaySound, SND_FILENAME, SND_ASYNC
from Tkinter import *
import random
import time

# dimensoes do canvas
LARGURA_CANVAS = 400
ALTURA_CANVAS = 600
# raio da bola em pixels
RAIO_BOLA = 10
# dimensoes dos tijolos
LARGURA_TIJOLO = 60
ALTURA_TIJOLO = 5

#dimensoes do coracao
LARG_CORACAO=10
ALT_CORACAO=10
# número de tentativas
TENTATIVAS = 3
PONTOS=0
#intervalo de animação
DELAY = 0.005
#componentes da velocidade da bola:
vy = 3
#componentes da velocidade dos tijolos:
vt=-3
x1=LARGURA_CANVAS/2 - RAIO_BOLA
y1=0

TIJOLOS=0
ARMADILHA=None

TIJOLO4=None
objColidido=None
CORACAO=None
tocouCORACAO= 'C:\Windows\Media\Savanna\Windows Default.wav'
tocouTIJOLO='C:\Windows\Media\Windows User Account Control.wav' 
BOLAfora= "C:\Windows\Media\Speech Sleep.wav"
perdeuJogo= "C:\Windows\Media\Raga\Windows Critical Stop.wav"
ganhouJogo= "C:\Windows\Media\tada.wav"
tocouARMADILHA="C:\Windows\Media\Raga\Windows Hardware Remove.wav"

def setup():
    global BOLA,TEXTO1,TEXTO2,TEXTO3
    #Criar a bola:
    BOLA= canvas.create_oval(x1,y1,
                       LARGURA_CANVAS/2+RAIO_BOLA, 2*RAIO_BOLA, fill='red')
    #Texto que instrui o jogador a iniciar o jogo:
    TEXTO1= canvas.create_text(LARGURA_CANVAS/2 , ALTURA_CANVAS/2 +2*RAIO_BOLA+ 20,
                                       font=('Times New Roman', 36),
                                       text = 'Clique para começar')

     #mostra ao jogador a quantidade restante de tentativas:
    TEXTO2= canvas.create_text( 10, 10,text=  'TENTATIVAS: ' + str(TENTATIVAS), anchor=NW, font=('Times New Roman', 14),fill='blue')

     #mostra ao jogador a quantidade de PONTOS:
    TEXTO3 = canvas.create_text( LARGURA_CANVAS-10,10,
                             text = 'PONTOS: %5d ' % (PONTOS),
                             anchor=NE, font=('Times New Roman', 14),fill='maroon')


def getX(objeto):
    [x0, y0, x1, y1] = canvas.coords(objeto)
    return x1

def getY(objeto):
    [x0, y0, x1, y1] = canvas.coords(objeto)
    return y1

def IniciouRodada():
    global BOLA, TENTATIVAS,vy,coracao
    while 0<getY(BOLA)<ALTURA_CANVAS+2*RAIO_BOLA:
        coracao=0
        moveBOLA()
        verificaObjColidido()
        administraCenario()
        moveTIJOLOS()
        if ColidiuArmadilha(): break
            
        if PONTOS>=1000:
            gameWon()
            return

    TENTATIVAS-=1
    canvas.itemconfig(TEXTO2, text = 'TENTATIVAS: ' + str(TENTATIVAS))
    tocaSom(BOLAfora)

    
    if TENTATIVAS!=0:
        canvas.delete(BOLA)
        BOLA= canvas.create_oval(LARGURA_CANVAS/2 - RAIO_BOLA,0,
                   LARGURA_CANVAS/2+RAIO_BOLA,2*RAIO_BOLA , fill='red')
        vy=3
    else:
        gameOver()
    

def moveBOLA():
    global PONTOS,vy
    canvas.move(BOLA, 0,vy)
    canvas.update() 
    time.sleep(DELAY)
    if objColidido==None:
        PONTOS+=1
    canvas.itemconfig(TEXTO3, text = 'PONTOS: %5d ' % (PONTOS))

def criaCenario():
    global TIJOLOS,TIJOLO1,TIJOLO2 ,TIJOLO3,TIJOLO4,TIJOLO5,CORACAO,x2,y2
    x2=random.uniform(0.0, LARGURA_CANVAS-LARGURA_TIJOLO)
    y2=ALTURA_CANVAS
    if TIJOLOS==0 :
       
        TIJOLO1=canvas.create_rectangle(x2,y2,x2+LARGURA_TIJOLO,y2-ALTURA_TIJOLO,
                            fill='black',tags='tijolo')
        TIJOLOS+=1

    if TIJOLOS==1 and getY(TIJOLO1)<ALTURA_CANVAS-100  :
        TIJOLO2=canvas.create_rectangle(x2,y2,x2+LARGURA_TIJOLO,y2-ALTURA_TIJOLO,
                            fill='black',tags='tijolo')
        TIJOLOS+=1

    if TIJOLOS==2 and getY(TIJOLO2)<ALTURA_CANVAS-200:
        TIJOLO3=canvas.create_rectangle(x2,y2,x2+LARGURA_TIJOLO,y2-ALTURA_TIJOLO,
                            fill='black',tags='tijolo')
        TIJOLOS+=1

    if TIJOLOS==3 and getY(TIJOLO3)<ALTURA_CANVAS-100  :
        TIJOLO4=canvas.create_rectangle(x2,y2,x2+LARGURA_TIJOLO,y2-ALTURA_TIJOLO,
                            fill='black',tags='tijolo')
        TIJOLOS+=1
        
        CORACAO=canvas.create_polygon(x2, y2-ALTURA_TIJOLO-LARG_CORACAO,x2+LARG_CORACAO,
                                          y2-ALTURA_TIJOLO-2*LARG_CORACAO,x2+2*LARG_CORACAO,
                                          y2-ALTURA_TIJOLO-LARG_CORACAO,x2+LARG_CORACAO,
                                          y2-ALTURA_TIJOLO,fill='magenta',
                                          outline='black',tags='tijolo') 
    if TIJOLOS==4 and getY(TIJOLO4)<ALTURA_CANVAS-100 :
        TIJOLO5=canvas.create_rectangle(x2,y2,x2+LARGURA_TIJOLO,y2-ALTURA_TIJOLO,
                            fill='black',tags='tijolo')
       
        TIJOLOS+=1
        
    


def moveTIJOLOS():
    canvas.move('tijolo',0,vt)
    canvas.update()
    time.sleep(DELAY)


def moveuMouse(e):
    global x1
    if not gameOver() and not gameWon():
    
        canvas.move(BOLA, e.x-RAIO_BOLA - x1 ,0 ) #move a bola na horizontal
        x1=e.x-RAIO_BOLA    
        if getX(BOLA) <= 2*RAIO_BOLA:
            canvas.move(BOLA, 2*RAIO_BOLA - getX(BOLA),0)
            x1=0
        if getX(BOLA)>=LARGURA_CANVAS:
            canvas.move(BOLA,LARGURA_CANVAS - getX(BOLA),0)
            x1=LARGURA_CANVAS-2*RAIO_BOLA

def clicouMouse(e): 
    if not gameOver() and not gameWon():
        canvas.delete(TEXTO1)
        IniciouRodada()



    
def verificaObjColidido():
    global vy,vt,objColidido
    objColidido = detectaColisoes()
    if objColidido != None:
        if objColidido !=CORACAO and objColidido!= TEXTO3 and objColidido!=TEXTO2 and objColidido!=ARMADILHA:
            if getY(BOLA) > getY(objColidido)-ALTURA_TIJOLO:
                dif = getY(BOLA)- getY(objColidido) + ALTURA_TIJOLO
                canvas.move(BOLA, 0, -dif)
            vy=vt
          
    else:
        vy=3
        
     



def detectaColisoes():
    global lista,TENTATIVAS
    [xb0, yb0, xb1, yb1] = canvas.coords(BOLA)
    lista = canvas.find_overlapping(xb0, yb0, xb1, yb1)
    for obj in lista:
        if obj ==CORACAO:
            tocaSom(tocouCORACAO)   
            TENTATIVAS+=1
            canvas.delete(CORACAO)
            canvas.itemconfig(TEXTO2, text = 'TENTATIVAS: ' + str(TENTATIVAS))
    if len(lista)>1:
        if lista[0] != BOLA  :
            return lista [0]
        elif lista[1] != BOLA :
            return lista[1]
        



def gameWon():
    if PONTOS>=1000:
        canvas.delete(BOLA)    
        canvas.create_text(LARGURA_CANVAS/2, ALTURA_CANVAS/2,
                                           font=('Comic Sans', 36),
                                           text = 'Parabéns,',fill='pink')

        canvas.create_text(LARGURA_CANVAS/2, ALTURA_CANVAS/2+ 100,
                                           font=('Comic Sans', 36),
                                           text = 'Você é bom!!',fill='pink')

        canvas.create_text(LARGURA_CANVAS/2,ALTURA_CANVAS/2 +200,
                                           text = 'em breve níveis mais difíceis..',
                                           font=('Comic Sans', 14))
        tocaSom(ganhouJogo)
        return True


def gameOver():
    if TENTATIVAS==0:
        canvas.delete('tijolo')
        canvas.delete(BOLA)
        canvas.create_text(LARGURA_CANVAS/2, ALTURA_CANVAS/2,
                                       font=('Courrier', 36),
                                       text = 'GAME OVER')
        tocaSom(perdeuJogo)
        return True

def tocaSom(file):
    PlaySound(file, SND_FILENAME|SND_ASYNC)

def administraCenario():
    global TIJOLO1,TIJOLO2,TIJOLO3,TIJOLO4,TIJOLO5,x2,CORACAO,ARMADILHA
    x2=random.uniform(0.0, LARGURA_CANVAS-LARGURA_TIJOLO)
    if TIJOLOS<5:
            criaCenario()
    
        
    elif TIJOLO1!=None and getY(TIJOLO1)<0:
        canvas.delete(TIJOLO1)
        TIJOLO1=canvas.create_rectangle(x2,y2,x2+LARGURA_TIJOLO,y2-ALTURA_TIJOLO,
                        fill='black',tags='tijolo')
        
     
    elif TIJOLO2!=None and getY(TIJOLO2)<0:
        canvas.delete(TIJOLO2)
        TIJOLO2=canvas.create_rectangle(x2,y2,x2+LARGURA_TIJOLO,y2-ALTURA_TIJOLO,
                        fill='black',tags='tijolo')
        
    elif TIJOLO3!=None and getY(TIJOLO3)<0:
        canvas.delete(TIJOLO3)
        
        TIJOLO3=canvas.create_rectangle(x2,y2,x2+LARGURA_TIJOLO,y2-ALTURA_TIJOLO,
                        fill='black',tags='tijolo')
        if random.choice([True, False])==True:
            CORACAO=canvas.create_polygon(x2, y2-ALTURA_TIJOLO-LARG_CORACAO,x2+LARG_CORACAO,
                                          y2-ALTURA_TIJOLO-2*LARG_CORACAO,x2+2*LARG_CORACAO,
                                          y2-ALTURA_TIJOLO-LARG_CORACAO,x2+LARG_CORACAO,
                                          y2-ALTURA_TIJOLO,fill='magenta',
                                          outline='black',tags='tijolo')
    elif TIJOLO4!=None and getY(TIJOLO4)<0:
        canvas.delete(TIJOLO4)
        TIJOLO4=canvas.create_rectangle(x2,y2,x2+LARGURA_TIJOLO,y2-ALTURA_TIJOLO,
                        fill='black',tags='tijolo')
   
        
    elif TIJOLO5!=None and getY(TIJOLO5)<0:
        canvas.delete(TIJOLO5)
        
        TIJOLO5=canvas.create_rectangle(x2,y2,x2+LARGURA_TIJOLO,y2-ALTURA_TIJOLO,
                        fill='black',tags='tijolo')
        
        
        

    if TIJOLO4!=None and ARMADILHA==None:
        ARMADILHA=canvas.create_rectangle(x2,y2,x2+LARGURA_TIJOLO,y2-ALTURA_TIJOLO,
                        fill='red',outline='magenta',tags='tijolo')
    elif ARMADILHA!=None and getY(ARMADILHA)<0:
            canvas.delete(ARMADILHA)
            ARMADILHA=canvas.create_rectangle(x2,y2,x2+LARGURA_TIJOLO,y2-ALTURA_TIJOLO,
                        fill='red',outline='magenta',tags='tijolo')

def ColidiuArmadilha():
    global TENTATIVAS
    for obj in lista:
        if obj ==ARMADILHA:
            tocaSom(tocouARMADILHA)   
            return True

        

canvas = Canvas(width=LARGURA_CANVAS, height=ALTURA_CANVAS,
background='cyan')
canvas.pack(fill=BOTH,expand=YES)

setup()

canvas.bind("<Motion>", moveuMouse)
canvas.bind("<ButtonPress>", clicouMouse)

mainloop()
