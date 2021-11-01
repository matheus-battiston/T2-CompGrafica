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
        self.velocidade = 10
        self.selecionado = 0
        self.parado = False
        self.inimigo = False
        self.xs =[0,-2,2]
        self.ys = [3,-3,-3]
        self.x1 = 0
        self.y1 = 3
        self.x2 = -2
        self.y2 = -3
        self.x3 = 2
        self.y3 = -3

    def get_pontos(self):
        curva_atual = self.curva
        if self.voltando ==0:
            if len(curvas[curva_atual]) == 3:
                a = curvas[curva_atual][0]
                b = curvas[curva_atual][1]
                c = curvas[curva_atual][2]
            elif len(curvas[curva_atual]) == 4:
                a = curvas[curva_atual][0]
                b = curvas[curva_atual][1]
                c = curvas[curva_atual][2]
                d = curvas[curva_atual][3]

        elif self.voltando == 1:
            if len(curvas[curva_atual]) == 3:
                a = curvas[curva_atual][2]
                b = curvas[curva_atual][1]
                c = curvas[curva_atual][0]

            elif len(curvas[curva_atual]) == 4:
                a = curvas[curva_atual][3]
                b = curvas[curva_atual][2]
                c = curvas[curva_atual][1]
                d = curvas[curva_atual][0]



        if len(curvas[curva_atual]) == 3:
            return a,b,c
        elif len(curvas[curva_atual]) == 4:
            return a,b,c,d



    def avanca(self):
        global pontos
        global curvas
        curva_atual = self.curva
        proxima_curva = self.proxima

        t = self.t
        pnts = self.get_pontos()


        if self.t <= 1:
            UmMenosT = 1 - t
            if len(pnts) == 3:
                b1,b2 = calc_bezier(pnts[0],pnts[1],pnts[2],t)
            elif len(pnts) == 4:
                b1,b2 = calc_bezier4(pnts[0],pnts[1],pnts[2],pnts[3],t)

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
                self.ponto_chegada = int(curvas[self.curva][len(curvas[self.curva])-1])
            else:
                self.ponto_saida = int(curvas[self.curva][len(curvas[self.curva])-1])
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
        self.xs[0] = self.xs[0] +self.x
        self.xs[1] = self.xs[1] +self.x
        self.xs[2] = self.xs[2] + self.x
        self.ys[0] = self.ys[0] + self.y
        self.ys[1] = self.y+self.ys[1]
        self.ys[2] = self.y+self.ys[2]

    def rotate(self,angulo):
        angulo = math.radians(angulo)
        
        
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

        pnts = self.get_pontos()

        if len(pnts) == 3:
            a = float(pontos[pnts[0]].x)
            b = float(pontos[pnts[1]].x)
            c = float(pontos[pnts[2]].x)
            ay = float(pontos[pnts[0]].y)
            by = float(pontos[pnts[1]].y)
            cy = float(pontos[pnts[2]].y)
            tangentex = 2*c*t - 2*b*t + 2*b*(1-t) - 2 * a*(1-t)
            tangentey = 2*cy*t - 2*by*t + 2*by*(1-t) - 2 * ay*(1-t)

        elif len(pnts) == 4:

            a = float(pontos[pnts[0]].x)
            b = float(pontos[pnts[1]].x)
            c = float(pontos[pnts[2]].x)
            d = float(pontos[pnts[3]].x)
            ay = float(pontos[pnts[0]].y)
            by = float(pontos[pnts[1]].y)
            cy = float(pontos[pnts[2]].y)
            dy = float(pontos[pnts[3]].y)
            tangentex = 3*d*t**2-3*c*t**2+6*c*(1-t)*t-6*b*(1-t)*t+3*b*(1-t)**2-3*a*(1-t)**2
            tangentey = 3*dy*t**2-3*cy*t**2+6*cy*(1-t)*t-6*by*(1-t)*t+3*by*(1-t)**2-3*ay*(1-t)**2

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
        ultimo = int(aux[len(aux)-1])
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

def calc_bezier4 (pnt1,pnt2,pnt3,pnt4,t):
        ponto1 = pontos[pnt1]
        ponto2 = pontos[pnt2]
        ponto3 = pontos[pnt3]
        ponto4 = pontos[pnt4]
        UmMenosT = 1 - t

        b1= (1-t)**3 * float(ponto1.x) + 3 * t * (1-t)**2 * float(ponto2.x) + 3 * t**2 * (1-t) * float(ponto3.x) + t**3 * float(ponto4.x)
        b2 = UmMenosT**3 * float(ponto1.y) + 3 * t * (UmMenosT)**2 * float(ponto2.y) + 3 * t**2 * (UmMenosT) * float(ponto3.y) + t**3 * float(ponto4.y)

        return(b1,b2)

def calculaDistancia(ponto1,ponto2):
    xa = ponto1[0]
    ya = ponto1[1]
    xb = ponto2[0]
    yb = ponto2[1]
    z = ((xb-xa)**2 + (yb-ya)**2)
    return z

def calculaComprimentoDaCurva(curva):

    if len(curvas[curva]) == 3:
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
    
    elif len(curvas[curva]) == 4:
        ponto1 = curvas[curva][0]
        ponto2 = curvas[curva][1]
        ponto3 = curvas[curva][2]
        ponto4 = curvas[curva][3]

        DeltaT = 1.0/50
        t=DeltaT
        ComprimentoTotalDaCurva = 0
        P1 = calc_bezier4(ponto1,ponto2,ponto3,ponto4,t)
        while(t<1.0):
            P2 = calc_bezier4(ponto1,ponto2,ponto3,ponto4,t)
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
            if len(pont) == 3:
                bez = calc_bezier (pont[0],pont[1],pont[2],t)
                bezier[index].append((bez[0],bez[1]))
                t += 0.001
            elif len(pont) == 4:
                bez = calc_bezier4(pont[0],pont[1],pont[2],pont[3],t)
                bezier[index].append((bez[0],bez[1]))
                t += 0.001

def desenha_bezier(indice):

    glBegin(GL_LINE_STRIP)
    for x in bezier[indice]:
        glVertex2f(x[0],x[1])

    glEnd()

def trac_bezier():
    global bezier
    t = 0
    glLineWidth(5)
    glShadeModel(GL_FLAT)

    for index, x in enumerate(bezier):

        if index == player.proxima:
            glColor3f(0,1,0)
            desenha_bezier(index)
        elif index == player.curva:
            glColor3f(0,0,1)
            desenha_bezier(index)
        else:
            glColor3f(1,0,0)
            desenha_bezier(index)


#**************************************************************************************************************************************


def primeira_curva():
    player.curva = random.randint(0,len(curvas)-1) 
    player.ponto_saida = curvas[player.curva][0]
    player.ponto_chegada = curvas[player.curva][len(curvas[player.curva])-1]

def inicializa_inimigos():
    global inimigos
    for x in range(0,5):
        inimigos.append(None)
    for index, i in enumerate(inimigos):
        inimigos[index] = Personagem()
        inimigos[index].t = random.random()
        inimigos[index].velocidade = 10
        inimigos[index].curva = random.randint(0,len(curvas)-1)
        inimigos[index].proxima = 0
        inimigos[index].inimigo = True
    
        if index < 5:
            inimigos[index].ponto_saida = curvas[inimigos[index].curva][0]
            inimigos[index].ponto_chegada = curvas[inimigos[index].curva][len(curvas[inimigos[index].curva])-1]
        else:
            inimigos[index].ponto_saida = curvas[inimigos[index].curva][len(curvas[inimigos[index].curva])-1]
            inimigos[index].ponto_chegada = curvas[inimigos[index].curva][0]
            inimigos[index].voltando = 1


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
    pontos = leitura("pontos2.txt")
    curvas = leituraCurvas("curvas2.txt")
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

# **********************************************************************
# display()
# Funcao que exibe os desenhos na tela
#
# **********************************************************************

def perdeu():
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

        if x.curva == player.curva:
            if HaInterseccao(PA,PB,PD,PE):
                print(1)
                return True
            elif HaInterseccao(PA,PB,PE,PF):
                print(2)
                return True
            elif HaInterseccao(PA,PB,PD,PF):
                print(3)
                return True
            elif HaInterseccao(PB,PC,PD,PE):
                print(4)
                return True
            elif (HaInterseccao(PB,PC,PD,PE)):
                print(5)
                return True
            elif HaInterseccao(PB,PC,PE,PF):
                print(6)
                return True
            elif HaInterseccao(PA,PC,PD,PE):
                print(7)
                return True
            elif HaInterseccao(PA,PC,PE,PF):
                print(8)
                return True
            elif HaInterseccao(PA,PC,PD,PF):
                print(9)
                return True
    return False

def display():
    global cont
    global pontos
    global inimigos
    # Limpa a tela com  a cor de fundo
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    trac_bezier()
    player.desenha_personagem()
    for x in inimigos:
        x.desenha_personagem()


    if player.parado == False:
        player.avanca()
    for x in inimigos:
        x.avanca()

    if perdeu():
        os._exit(0)



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
        if player.parado == True:
            player.parado = False
        else:
            player.parado = True
        
        
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