#Alunos: Matheus Felipe Battiston e Henrique Andreata
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import random
import math
import timeit
from Ponto import Ponto

MAX_X = 100
pontos = []
inimigos = []
decisao = []
tamanho_curva = []
bezier = []

class Personagem:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.t = 0
        self.z = 0
        self.curva = 0
        self.proxima = 99
        self.inicio = 99
        self.vai_voltar = 0
        self.voltando = 0
        self.ponto_saida = 0
        self.ponto_chegada = 3
        self.velocidade = 30
        self.selecionado = 0
        self.parado = 0
        self.inimigo = False
        self.xs =[0,-2,2]
        self.ys = [3,-3,-3]
        self.x1 = 0
        self.y1 = 3
        self.x2 =-2
        self.y2 = -3
        self.x3 = 2
        self.y3 = -3

    def avanca(self):
        global pontos
        global curvas
        curva_atual = self.curva

        proxima_curva = self.proxima

        t = self.t
        if self.voltando == 0:

            ponto1x = pontos[curvas[curva_atual][0]].x
            ponto2x = pontos[curvas[curva_atual][1]].x
            ponto3x = pontos[curvas[curva_atual][2]].x
            ponto1y = pontos[curvas[curva_atual][0]].y
            ponto2y = pontos[curvas[curva_atual][1]].y
            ponto3y = pontos[curvas[curva_atual][2]].y 
        elif self.voltando == 1:
            ponto1x = pontos[curvas[curva_atual][2]].x
            ponto2x = pontos[curvas[curva_atual][1]].x
            ponto3x = pontos[curvas[curva_atual][0]].x
            ponto1y = pontos[curvas[curva_atual][2]].y
            ponto2y = pontos[curvas[curva_atual][1]].y
            ponto3y = pontos[curvas[curva_atual][0]].y 
            

        if self.t <= 1:
            UmMenosT = 1 - t
            b1 = float(ponto1x) * UmMenosT * UmMenosT + float(ponto2x) * 2 * UmMenosT * t + float(ponto3x) * t*t
            b2 = float(ponto1y) * UmMenosT * UmMenosT + float(ponto2y) * 2 * UmMenosT * t + float(ponto3y) * t*t
            self.x = b1
            self.y = b2
            deltat = (self.velocidade * 0.033)/tamanho_curva[self.curva]
            self.t = round(self.t + deltat, 10)
        if self.t >= 1:
            self.t = 0
            self.selecionado = 0
            self.voltando = self.vai_voltar
            self.vai_voltar = 0 
            self.curva = self.proxima
            if self.voltando == 0:
                self.ponto_saida = int(curvas[self.curva][0])
                self.ponto_chegada = int(curvas[self.curva][2])
            else:
                self.ponto_saida = int(curvas[self.curva][2])
                self.ponto_chegada = int(curvas[self.curva][0])
            

        if self.t >= 0.5 and self.selecionado != 1 :
            self.prox_curva()
            self.selecionado = 1

    def prox_curva(self):
        global decisao
        curva_atual = self.curva
        ponto_final = self.ponto_chegada
        aleatorio = random.randint(0,len(decisao[ponto_final])-1)
        self.proxima = decisao[ponto_final][aleatorio]

        if self.ponto_chegada == curvas[self.proxima][0]:
            self.vai_voltar = 0
        else:
            self.vai_voltar = 1

    def select_nova_curva(self):
        curva_atual = self.curva
        ponto_final = self.ponto_chegada
        proxima = self.proxima

        if len(decisao[ponto_final]) == 1:
            pass
        else:
            if self.proxima == 99:
                self.proxima = decisao[ponto_final][0]
            index = decisao[ponto_final].index(self.proxima)
            if index == len(decisao[ponto_final])-1:
                self.proxima = decisao[ponto_final][0]
            else:
                self.proxima = decisao[ponto_final][index+1]
        
            if self.ponto_chegada == curvas[self.proxima][0]:
                self.vai_voltar = 0
            else:
                self.vai_voltar = 1

    def voltar(self):
        if self.voltando == 1:
            self.voltando = 0
        else:
            self.voltando = 1
        self.selecionado = 0
        self.t = 1-self.t
        aux = self.ponto_chegada
        self.ponto_chegada = self.ponto_saida
        self.ponto_saida = aux
        self.proxima = 99
        if self.t >= 0.5:
            self.prox_curva()
            self.selecionado = 1

    def translate(self):
        self.xs[0] = self.x
        self.xs[1] = self.x -2
        self.xs[2] = self.x + 2
        self.ys[0] = self.y + 3
        self.ys[1] = -3+self.y
        self.ys[2] = -3 +self.y

    def rotate(self,angulo):
        angulo = math.radians(-angulo)
        
        self.xs[0] = (self.x1 * math.cos(angulo) - self.y1 * math.sin(angulo))
        self.ys[0] = (self.x1 * math.sin(angulo) + self.y1 * math.cos(angulo))
        self.xs[1] = (self.x2 * math.cos(angulo) - self.y2 * math.sin(angulo))
        self.ys[1] = (self.x2 * math.sin(angulo) + self.y2 * math.cos(angulo))
        self.xs[2] = (self.x3 * math.cos(angulo) - self.y3 * math.sin(angulo))
        self.ys[2] = (self.x3 * math.sin(angulo) + self.y3 * math.cos(angulo))
                 
    def desenha_personagem(self):
        tangente = self.calcula_pontos_tgt()
        rota = self.calcula_angulo_rotacao(tangente)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glTranslatef(self.x,self.y,0)
        glRotatef(-rota,0,0,1)
        self.rotate(rota)
        self.translate()



        glBegin(GL_TRIANGLES)
        if self.inimigo == True:
            glColor(0,1,0)
        else:
            glColor(0,0,1)
        glVertex2f(0,3)
        glVertex2f(-2,-3)
        glVertex2f(2,-3)

        glEnd()


    def calcula_pontos_tgt(self):
        global pontos, curvas
        t = self.t
        curva_atual = self.curva
        if self.voltando ==0:
            a = pontos[curvas[curva_atual][0]].x
            b = pontos[curvas[curva_atual][1]].x
            c = pontos[curvas[curva_atual][2]].x
            ay = pontos[curvas[curva_atual][0]].y
            by = pontos[curvas[curva_atual][1]].y
            cy = pontos[curvas[curva_atual][2]].y 
        else:
            a = pontos[curvas[curva_atual][2]].x
            b = pontos[curvas[curva_atual][1]].x
            c = pontos[curvas[curva_atual][0]].x
            ay = pontos[curvas[curva_atual][2]].y
            by = pontos[curvas[curva_atual][1]].y
            cy = pontos[curvas[curva_atual][0]].y 


        a = float(a)
        b = float(b)
        c = float(c)
        ay = float(ay)
        by = float(by)
        cy = float(cy)
        tangentex = 2*c*t - 2*b*t + 2*b*(1-t) - 2 * a*(1-t)
        tangentey = 2*cy*t - 2*by*t + 2*by*(1-t) - 2 * ay*(1-t)

        return tangentex,tangentey

    def calcula_angulo_rotacao(self,pontostgt):
        angulo = math.atan2(pontostgt[0],pontostgt[1])
        angulo = math.degrees(angulo)

        return angulo

#**************************************************************************************************************************
#Leituras

player = Personagem()
curvas = []



def leitura(arquivo):
    ponto = []
    arq = open(arquivo)
    linhas = arq.readlines()
    n_pontos = int(linhas.pop(0))
    for x in range (0,n_pontos):
        ponto.append(())
        ponto[x] = Ponto()
    count = 0

    for index, line in enumerate(linhas):
        aux = line.split(' ')
        ponto[index].set(aux[0],aux[1])

    arq.close()
    return ponto

def leituraCurvas(arquivo):
    global decisao
    curvas = []
    curva = []
    arq = open(arquivo)
    linhas = arq.readlines()
    n_curvas = int(linhas.pop(0))

    for x in range (0,len(pontos)):
        decisao.append([])
    
    for index, line in enumerate(linhas):
        aux = line.split(' ')
        primeiro = int(aux[0])
        ultimo = int(aux[2])
        if index not in decisao[primeiro]:
            decisao[primeiro].append(index)
        if index not in decisao[ultimo]:
            decisao[ultimo].append(index)

        for ponto in aux:
            curva.append(int(ponto.replace('\n', '')))
        curvas.append(curva)
        curva = []
  
    arq.close()
    return curvas

#**************************************************************************************************************************************

#**************************************************************************************************************************************
#Calculos

def calc_bezier(pnt1,pnt2,pnt3,t):
        ponto1 = pontos[pnt1]
        ponto2 = pontos[pnt2]
        ponto3 = pontos[pnt3]
        UmMenosT = 1 - t
        b1 = float(ponto1.x) * UmMenosT * UmMenosT + float(ponto2.x) * 2 * UmMenosT * t + float(ponto3.x) * t*t
        b2 = float(ponto1.y) * UmMenosT * UmMenosT + float(ponto2.y) * 2 * UmMenosT * t + float(ponto3.y) * t*t

        return(b1,b2)

def calculaDistancia(ponto1,ponto2):
    xa = ponto1[0]
    ya = ponto1[1]
    xb = ponto2[0]
    yb = ponto2[1]
    z = ((xb-xa)**2 + (yb-ya)**2)
    return z

def calculaComprimentoDaCurva(curva):

    ponto1 = curvas[curva][0]
    ponto2 = curvas[curva][1]
    ponto3 = curvas[curva][2]

    DeltaT = 1.0/50
    t=DeltaT
    ComprimentoTotalDaCurva = 0
    P1 = calc_bezier(ponto1,ponto2,ponto3,t)
    while(t<1.0):
        P2 = calc_bezier(ponto1,ponto2,ponto3,t)
        ComprimentoTotalDaCurva += calculaDistancia(P1,P2)
        P1 = P2
        t += DeltaT

    ComprimentoTotalDaCurva += calculaDistancia(P1,P2)
    return ComprimentoTotalDaCurva

def comprimentos():
    global curvas
    for index, x in enumerate(curvas):
        comprimento = calculaComprimentoDaCurva(index)
        tamanho_curva.append(comprimento)
        

#**************************************************************************************************************************************


#**************************************************************************************************************************************
#Desenhos

def define_bezier():
    global bezier
    for x in range (0,len(curvas)):
        bezier.append([])
    for index, pont in enumerate(curvas):
        t = 0
        while t <= 1:
            bez = calc_bezier (pont[0],pont[1],pont[2],t)
            bezier[index].append((bez[0],bez[1]))
            t += 0.001

def trac_bezier():
    t = 0
    glLineWidth(5)
    glShadeModel(GL_FLAT)
    glBegin(GL_LINE_STRIP)
    
    for index, x in enumerate(bezier):
        for y in x:
            if index == player.proxima:
                glColor3f(0, 1, 0)
            else:
                glColor3f(1, 0, 0)

            glVertex2f(y[0],y[1])

    glEnd()


#**************************************************************************************************************************************


def primeira_curva():
    player.curva = random.randint(0,len(curvas)-1) 
    player.ponto_saida = curvas[player.curva][0]
    player.ponto_chegada = curvas[player.curva][2]

def inicializa_inimigos():
    global inimigos
    for x in range(0,10):
        inimigos.append(None)
    for index, i in enumerate(inimigos):
        inimigos[index] = Personagem()
        inimigos[index].t = random.random()
        inimigos[index].velocidade = 30
        inimigos[index].curva = random.randint(0,len(curvas)-1)
        inimigos[index].proxima = 0
        inimigos[index].ponto_saida = curvas[inimigos[index].curva][0]
        inimigos[index].ponto_chegada = curvas[inimigos[index].curva][2]
        inimigos[index].inimigo = True


def intersec2d(k: Ponto, l: Ponto, m: Ponto, n: Ponto):
    det = (n.x - m.x) * (l.y - k.y)  -  (n.y - m.y) * (l.x - k.x)

    if (det == 0.0):
        return 0, None, None # não há intersecção

    s = ((n.x - m.x) * (m.y - k.y) - (n.y - m.y) * (m.x - k.x))/ det
    t = ((l.x - k.x) * (m.y - k.y) - (l.y - k.y) * (m.x - k.x))/ det

    return 1, s, t # há intersecção

# **********************************************************************
# HaInterseccao(k: Ponto, l: Ponto, m: Ponto, n: Ponto)
# Detecta interseccao entre os pontos
#
# **********************************************************************
def HaInterseccao(k: Ponto, l: Ponto, m: Ponto, n: Ponto) -> bool:
    ret, s, t = intersec2d( k,  l,  m,  n)

    if not ret: return False

    return s>=0.0 and s <=1.0 and t>=0.0 and t<=1.0


def init():

    global pontos
    global curvas
    
    # Define a cor do fundo da tela (BRANCO) 
    glClearColor(1.0, 1.0, 1.0, 1.0)
    pontos = leitura("pontos.txt")
    curvas = leituraCurvas("Curvas.txt")
    define_bezier()
    inicializa_inimigos()
    comprimentos()
    primeira_curva()

   
# **********************************************************************
#  reshape( w: int, h: int )
#  trata o redimensionamento da janela OpenGL
#
# **********************************************************************

def reshape(w: int, h: int):
    # Reseta coordenadas do sistema antes the modificala
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Define os limites lógicos da área OpenGL dentro da Janela
    glOrtho(0, 100, 0, 100, 0, 1)

    # Define a área a ser ocupada pela área OpenGL dentro da Janela
    glViewport(0, 0, w, h)

    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


# **********************************************************************
# DesenhaLinhas()
# Desenha as linha na tela
#
# **********************************************************************

# **********************************************************************
# DesenhaCenario()
# Desenha o cenario
#
# **********************************************************************

def DesenhaCenario():
    global ContChamadas, ContadorInt
    ContChamadas, ContadorInt = 0, 0
    
    # Desenha as linhas do cenário
    glLineWidth(1)
    glColor3f(1,0,0)


# **********************************************************************
# display()
# Funcao que exibe os desenhos na tela
#
# **********************************************************************
def colisao_envelope(ini,play):
    if (abs(ini.x - play.x) > 2 + 2):
        return False
    elif abs(ini.y - ini.y) > 3 + 3:
        return False

    return True 
    
def perdeu2():
    PA = Ponto()
    PB = Ponto()
    PC = Ponto()
    PD = Ponto()
    PE = Ponto()
    PF = Ponto()

    PA.set(player.xs[0],player.ys[0])
    PB.set(player.xs[1],player.ys[1])
    PC.set(player.xs[2],player.ys[2])

    for x in inimigos:

        PD.set(x.xs[0],x.ys[0])
        PE.set(x.xs[1],x.ys[1])
        PF.set(x.xs[2],x.ys[2])

        if x.voltando == 1:
            init = 1 - x.t
        else:
            init = x.t

        if player.voltando == 1:
            playt = 1-player.t
        else:
            playt = player.t


        difabs = abs(init-playt)
        difabs = round(difabs,3)


        if x.curva == player.curva and difabs <= 0.1:
            if HaInterseccao(PA,PB,PE,PF):
                return True
            elif HaInterseccao(PA,PB,PD,PE):
                return True
            elif HaInterseccao(PB,PC,PD,PE):
                return True
            elif HaInterseccao(PB,PC,PD,PF):
                return True
 
    return False

avanco = 0
def display():
    global avanco
    global cont
    global pontos
    global inimigos
    # Limpa a tela com  a cor de fundo
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    trac_bezier()
    DesenhaCenario()
    player.desenha_personagem()
    for x in inimigos:
        x.desenha_personagem()

    

    avanco += 1





    glutSwapBuffers()


# **********************************************************************
# animate()
# Funcao chama enquanto o programa esta ocioso
# Calcula o FPS e numero de interseccao detectadas, junto com outras informacoes
#
# **********************************************************************
# Variaveis Globais
nFrames, TempoTotal, AccumDeltaT = 0, 0, 0
oldTime = time.time()

def animate():
    global nFrames, TempoTotal, AccumDeltaT, oldTime
    nowTime = time.time()
    dt = nowTime - oldTime
    oldTime = nowTime

    AccumDeltaT += dt
    TempoTotal += dt
    nFrames += 1
    
    if AccumDeltaT > 1.0/30:  # fixa a atualização da tela em 30
        AccumDeltaT = 0
        glutPostRedisplay()


    if player.parado == 0:
        player.avanca()
    for x in inimigos:
        x.avanca()

    if avanco >3:
        if perdeu2():
            os._exit(0)

# **********************************************************************
#  keyboard ( key: int, x: int, y: int )
#
# **********************************************************************
ESCAPE = b'\x1b'
def keyboard(*args):
    #print (args)
    # If escape is pressed, kill everything.

    if args[0] == ESCAPE:   # Termina o programa qdo
        os._exit(0)         # a tecla ESC for pressionada

    if args[0] == b' ':
        if player.parado == 0:
            player.parado = 1
        else:
            player.parado = 0
        
        
    # Força o redesenho da tela
    glutPostRedisplay()

# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )
#
#
# **********************************************************************

def arrow_keys(a_keys: int, x: int, y: int):
    global Subdivisoes
    global Cel
    global linhas

    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        pass
    if a_keys == GLUT_KEY_DOWN:      # Se pressionar DOWN
        player.select_nova_curva ()
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        player.voltar()
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        pass

    glutPostRedisplay()


def mouse(button: int, state: int, x: int, y: int):
    glutPostRedisplay()

def mouseMove(x: int, y: int):
    glutPostRedisplay()

# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowPosition(0, 0)

# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(700, 700)
# Cria a janela na tela, definindo o nome da
# que aparecera na barra de título da janela.
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Algorimos de Cálculo de Colisão")

# executa algumas inicializações
init ()

# Define que o tratador de evento para
# o redesenho da tela. A funcao "display"
# será chamada automaticamente quando
# for necessário redesenhar a janela
glutDisplayFunc(display)
glutIdleFunc (animate)

# o redimensionamento da janela. A funcao "reshape"
# Define que o tratador de evento para
# será chamada automaticamente quando
# o usuário alterar o tamanho da janela
glutReshapeFunc(reshape)

# Define que o tratador de evento para
# as teclas. A funcao "keyboard"
# será chamada automaticamente sempre
# o usuário pressionar uma tecla comum
glutKeyboardFunc(keyboard)
    
# Define que o tratador de evento para
# as teclas especiais(F1, F2,... ALT-A,
# ALT-B, Teclas de Seta, ...).
# A funcao "arrow_keys" será chamada
# automaticamente sempre o usuário
# pressionar uma tecla especial
glutSpecialFunc(arrow_keys)

#glutMouseFunc(mouse)
#glutMotionFunc(mouseMove)


try:
    # inicia o tratamento dos eventos
    glutMainLoop()
except SystemExit:
    pass