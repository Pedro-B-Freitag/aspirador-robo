import random

class Quarto:
    TAMANHO = 6
    PAREDE = 1
    LIMPO = 0
    SUJO = 2

    def __init__(self):
        self.matriz = self._gerar_quarto()

    def _gerar_quarto(self):
        matriz = [[self.PAREDE] * self.TAMANHO for _ in range(self.TAMANHO)]

        posicoes_internas = []
        for linha in range(1, self.TAMANHO - 1):
            for coluna in range(1, self.TAMANHO - 1):
                posicoes_internas.append((linha, coluna))

        for linha, coluna in posicoes_internas:
            matriz[linha][coluna] = self.LIMPO

        qtd_sujeiras = random.randint(1, len(posicoes_internas) - 1)
        posicoes_sujas = random.sample(posicoes_internas, qtd_sujeiras)

        for linha, coluna in posicoes_sujas:
            matriz[linha][coluna] = self.SUJO

        return matriz

    def exibir(self):
        for linha in self.matriz:
            print(" ".join(str(valor) for valor in linha))