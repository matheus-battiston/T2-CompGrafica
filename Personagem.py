class Personagem:
    def __init__(self):
        self.xinicial = 0
        self.yinicial = 0
        self.x = 0
        self.y = 0
        self.t = 0
        self.x2 = self.x + 1
        self.y2 = self.y + 3
        self.x3 = self.x -1
        self.y3 = self.y - 3
        self.z = 0
        self.curva = 0
        self.proxima = 99
        self.inicio = 99
        self.vai_voltar = 0
        self.voltando = 0
        self.ponto_saida = 0
        self.ponto_chegada = 3

    def atualiza(self):
        self.x2 = self.x + 1
        self.y2 = self.y + 3
        self.x3 = self.x -1
        self.y3 = self.y - 3
    



    