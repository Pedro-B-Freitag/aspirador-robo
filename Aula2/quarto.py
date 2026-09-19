import random

class Quarto:
    TAMANHO = 4
    LIMPO = 0
    SUJO = 2
    MINIMO_SUJEIRAS = 1

    def __init__(self):
        self.matriz = self._gerar_quarto()

    def _gerar_quarto(self):
        matriz = [[self.LIMPO] * self.TAMANHO for _ in range(self.TAMANHO)]
        posicoes = [
            (linha, coluna)
            for linha in range(self.TAMANHO)
            for coluna in range(self.TAMANHO)
        ]

        qtd_sujeiras = random.randint(self.MINIMO_SUJEIRAS, len(posicoes) - 1)
        posicoes_sujas = random.sample(posicoes, qtd_sujeiras)

        for linha, coluna in posicoes_sujas:
            matriz[linha][coluna] = self.SUJO

        return matriz

    def exibir(self):
        for linha in self.matriz:
            print(" ".join(str(valor) for valor in linha))