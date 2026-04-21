class AmbienteMario:
    def __init__(self):
        self.largura = 50
        self.altura = 6
        self.chao_y = 5
        self.fim_x = 47

        self.obstaculos = {8, 15, 21, 29, 36, 43}
        self.buracos = {11, 12, 18, 19, 25, 26, 33, 34, 39, 40}

        self.reset()

    def reset(self):
        self.mario_x = 0
        self.mario_y = self.chao_y - 1
        self.vel_y = 0
        self.no_chao = True
        self.vivo = True
        self.venceu = False
        self.passos = 0

    def aplicar_acao(self, acao):
        if not self.vivo or self.venceu:
            return

        if acao in (1, 3):
            self.mario_x += 1
            if self.mario_x >= self.largura:
                self.mario_x = self.largura - 1

        if acao in (2, 3) and self.no_chao:
            self.vel_y = -2
            self.no_chao = False

        self.mario_y += self.vel_y
        self.vel_y += 1

        if self.mario_y < 0:
            self.mario_y = 0

        chao_existe = self.mario_x not in self.buracos

        if chao_existe:
            if self.mario_y >= self.chao_y - 1:
                self.mario_y = self.chao_y - 1
                self.vel_y = 0
                self.no_chao = True
            else:
                self.no_chao = False
        else:
            self.no_chao = False
            if self.mario_y >= self.altura:
                self.vivo = False

        if self.mario_x in self.obstaculos and self.mario_y == self.chao_y - 1:
            self.vivo = False

        if self.mario_x >= self.fim_x:
            self.venceu = True

        self.passos += 1

    def simular(self, acoes):
        self.reset()
        for acao in acoes:
            self.aplicar_acao(acao)
            if not self.vivo or self.venceu:
                break
        return self.obter_resultado()

    def obter_resultado(self):
        return {
            "x": self.mario_x,
            "y": self.mario_y,
            "vivo": self.vivo,
            "venceu": self.venceu,
            "passos": self.passos,
        }

    def calcular_fitness(self, resultado):
        fitness = resultado["x"] * 10 + resultado["passos"]

        if resultado["venceu"]:
            fitness += 1000

        if not resultado["vivo"] and not resultado["venceu"]:
            fitness -= 200

        return fitness

    def avaliar_individuo(self, acoes):
        resultado = self.simular(acoes)
        fitness = self.calcular_fitness(resultado)
        return fitness, resultado

    def render_texto(self):
        grade = [["." for _ in range(self.largura)] for _ in range(self.altura)]

        for x in range(self.largura):
            if x not in self.buracos:
                grade[self.chao_y][x] = "#"

        for x in self.obstaculos:
            if 0 <= x < self.largura:
                grade[self.chao_y - 1][x] = "X"

        if 0 <= self.fim_x < self.largura:
            grade[self.chao_y - 1][self.fim_x] = "F"

        if 0 <= self.mario_y < self.altura and 0 <= self.mario_x < self.largura:
            grade[self.mario_y][self.mario_x] = "M"

        return "\n".join("".join(linha) for linha in grade)