from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time

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
    curvas = []
    curva = []
    arq = open(arquivo)
    linhas = arq.readlines()
    n_curvas = int(linhas.pop(0))


    for index, line in enumerate(linhas):
        aux = line.split(' ')
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
    # Define a cor do fundo da tela (BRANCO) 
    glClearColor(1.0, 1.0, 1.0, 1.0)
    pontos = leitura("pontos.txt")
    curvas = leituraCurvas("Curvas.txt")
    player.x = float(pontos[1].x)
    player.y = float(pontos[1].y)
    

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
    for pont in curvas:
        if len(pont) == 3:
            ponto1 = (pontos[pont[0]].x,pontos[pont[0]].y)
            ponto2 = (pontos[pont[1]].x,pontos[pont[1]].y)
            ponto3 = (pontos[pont[2]].x,pontos[pont[2]].y)
            t = 0.0

            while t <= 1:
                UmMenosT = 1 - t
                b1 = float(ponto1[0]) * UmMenosT * UmMenosT + float(ponto2[0]) * 2 * UmMenosT * t + float(ponto3[0]) * t*t
                b2 = float(ponto1[1]) * UmMenosT * UmMenosT + float(ponto2[1]) * 2 * UmMenosT * t + float(ponto3[1]) * t*t
                desenha(b1,b2)
                t += 0.001

def desenha(x,y):
    glPointSize(4)
    glColor3d(1, 0, 0)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
  
    glEnd()

def desenha_player():
    x = float(player.x)
    y = float(player.y)
    glBegin(GL_TRIANGLES)

    glColor3f(0.5,0,0)

    glVertex2f(x,y)
    glVertex2f(x-1,y-3)
    glVertex2f(x+1,y-3)

    glEnd()

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
    global pontos
    time.sleep(0.1)

    t = player.t
    ponto1x = pontos[1].x
    ponto2x = pontos[2].x
    ponto3x = pontos[3].x
    ponto1y = pontos[1].y
    ponto2y = pontos[2].y
    ponto3y = pontos[3].y
    if player.t <= 1:
        UmMenosT = 1 - t
        b1 = float(ponto1x) * UmMenosT * UmMenosT + float(ponto2x) * 2 * UmMenosT * t + float(ponto3x) * t*t
        b2 = float(ponto1y) * UmMenosT * UmMenosT + float(ponto2y) * 2 * UmMenosT * t + float(ponto3y) * t*t
    player.x = b1
    player.y = b2
    player.t += 0.01

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
        
        print(f'Contador de Intersecoes Existentes: {ContadorInt/2.0}')
        print(f'Contador de Chamadas: {ContChamadas}')
        print( f'Subdivisões', Subdivisoes)

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
glutInitWindowSize(1366, 768)
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