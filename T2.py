from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import random
import math

from Ponto import Ponto
from Personagem import Personagem

MAX_X = 100
N_LINHAS= 5000
ContadorInt = 0
ContChamadas = 0
Subdivisoes = 10

linhas = []
Lista_Faixas_X = []
Lista_Faixas_Y = []
ListaFinal = []
pontos = []
curvas = []
player = Personagem()
teste = 0
decisao = []

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


def init():

    global pontos
    global curvas
    global player
    global decisao
    # Define a cor do fundo da tela (BRANCO) 
    glClearColor(1.0, 1.0, 1.0, 1.0)
    pontos = leitura("pontos.txt")
    curvas = leituraCurvas("Curvas.txt")
    player.x = float(pontos[curvas[0][0]].x)
    player.y = float(pontos[curvas[0][0]].x)
    player.curva = 0
    print(decisao)


    print(curvas)
    

    
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

def bezier():
    global pontos
    for index, pont in enumerate(curvas):
        if len(pont) == 3:
            ponto1 = (pontos[pont[0]].x,pontos[pont[0]].y)
            ponto2 = (pontos[pont[1]].x,pontos[pont[1]].y)
            ponto3 = (pontos[pont[2]].x,pontos[pont[2]].y)
            t = 0.0

            while t <= 1:
                UmMenosT = 1 - t
                b1 = float(ponto1[0]) * UmMenosT * UmMenosT + float(ponto2[0]) * 2 * UmMenosT * t + float(ponto3[0]) * t*t
                b2 = float(ponto1[1]) * UmMenosT * UmMenosT + float(ponto2[1]) * 2 * UmMenosT * t + float(ponto3[1]) * t*t
                desenha(b1,b2,index)
                t += 0.001

def desenha(x,y,index):
    glPointSize(4)
    if index == player.proxima:
        glColor3d(0, 1, 0)
    else:
        glColor3d(1, 0, 0)

    
    glBegin(GL_POINTS)
    glVertex2f(x,y)
  
    glEnd()

def desenha_player():

    t = player.t
    curva_atual = player.curva
    if player.voltando ==0:
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
    tangente = 2*c*t - 2*b*t + 2*b*(1-t) - 2 * a*(1-t)
    tangentey = 2*cy*t - 2*by*t + 2*by*(1-t) - 2 * ay*(1-t)

    angulo = math.atan2(tangente,tangentey)
    angulo = math.degrees(angulo)


    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(player.x,player.y,0)
    glRotatef(-angulo,0,0,1)

    glBegin(GL_TRIANGLES)

    glColor3f(0,0,1)
    glVertex2f(0,3)
    glVertex2f(-2,-3)
    glVertex2f(2,-3)


    glEnd()

    glutSwapBuffers()






def display():
    global pontos
    # Limpa a tela com  a cor de fundo
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    bezier()
    DesenhaCenario()
    desenha_player()

    glutSwapBuffers()

def avanca():
    global teste
    global pontos
    global curvas
    curva_atual = player.curva
    proxima_curva = player.proxima
    time.sleep(0.01)

    t = player.t
    if player.voltando == 0:
        ponto1x = pontos[curvas[curva_atual][0]].x
        ponto2x = pontos[curvas[curva_atual][1]].x
        ponto3x = pontos[curvas[curva_atual][2]].x
        ponto1y = pontos[curvas[curva_atual][0]].y
        ponto2y = pontos[curvas[curva_atual][1]].y
        ponto3y = pontos[curvas[curva_atual][2]].y 
    elif player.voltando == 1:
        ponto1x = pontos[curvas[curva_atual][2]].x
        ponto2x = pontos[curvas[curva_atual][1]].x
        ponto3x = pontos[curvas[curva_atual][0]].x
        ponto1y = pontos[curvas[curva_atual][2]].y
        ponto2y = pontos[curvas[curva_atual][1]].y
        ponto3y = pontos[curvas[curva_atual][0]].y 
          

    if player.t <= 1:
        UmMenosT = 1 - t
        b1 = float(ponto1x) * UmMenosT * UmMenosT + float(ponto2x) * 2 * UmMenosT * t + float(ponto3x) * t*t
        b2 = float(ponto1y) * UmMenosT * UmMenosT + float(ponto2y) * 2 * UmMenosT * t + float(ponto3y) * t*t
        player.x = b1
        player.y = b2
        player.t = round(player.t + 0.01, 2)
    if player.t >= 1:
        player.voltando = player.vai_voltar
        player.vai_voltar = 0 
        player.curva = player.proxima
        player.proxima = 99
        if player.voltando == 0:
            player.ponto_saida = int(curvas[player.curva][0])
            player.ponto_chegada = int(curvas[player.curva][2])
        else:
            player.ponto_saida = int(curvas[player.curva][2])
            player.ponto_chegada = int(curvas[player.curva][0])

        player.t = 0
    if player.t == 0.5:
        curva_atual = player.curva
        ponto_final = player.ponto_chegada
        aleatorio = random.randint(0,len(decisao[ponto_final])-1)
        player.proxima = decisao[ponto_final][aleatorio]

        if player.ponto_chegada == curvas[player.proxima][0]:
            player.vai_voltar = 0
        else:
            player.vai_voltar = 1


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

    if TempoTotal > 5.0:
        print(f'Tempo Acumulado: {TempoTotal} segundos.')
        print(f'Nros de Frames sem desenho: {int(nFrames)}')
        print(f'FPS(sem desenho): {int(nFrames/TempoTotal)}')
        
        TempoTotal = 0
        nFrames = 0


    avanca()

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
        init()

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
        if Subdivisoes < 50:
            pass
        else:
            pass
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        pass
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        pass
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