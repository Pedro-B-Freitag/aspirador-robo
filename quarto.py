import random

TAMANHO = 6
PAREDE = 1
LIMPO = 0
SUJO = 2

DIRECOES = {
    "acima": (-1, 0),
    "abaixo": (1, 0),
    "esquerda": (0, -1),
    "direita": (0, 1)
}


def todas_posicoes():
    posicoes = []
    for linha in range(1, TAMANHO - 1):
        for coluna in range(1, TAMANHO - 1):
            posicoes.append((linha, coluna))
    return posicoes


def gerar_sala():
    sala = [[PAREDE] * TAMANHO for _ in range(TAMANHO)]

    posicoes = todas_posicoes()
    for linha, coluna in posicoes:
        sala[linha][coluna] = LIMPO

    quantidade = random.randint(1, len(posicoes))
    for linha, coluna in random.sample(posicoes, quantidade):
        sala[linha][coluna] = SUJO

    return sala


def sortear_posicao():
    return random.choice(todas_posicoes())


def esta_sujo(sala, posicao):
    linha, coluna = posicao
    return sala[linha][coluna] == SUJO


def aspirar(sala, posicao):
    linha, coluna = posicao
    sala[linha][coluna] = LIMPO


def mover(sala, posicao, acao):
    linha, coluna = posicao
    d_linha, d_coluna = DIRECOES[acao]

    destino_linha = linha + d_linha
    destino_coluna = coluna + d_coluna

    if sala[destino_linha][destino_coluna] == PAREDE:
        return posicao

    return (destino_linha, destino_coluna)


def checkObj(sala):
    for linha in sala:
        if SUJO in linha:
            return 1
    return 0


def exibir(sala, posicao):
    for indice_linha, linha in enumerate(sala):
        valores = []
        for indice_coluna, valor in enumerate(linha):
            if (indice_linha, indice_coluna) == posicao:
                valores.append("A")
            else:
                valores.append(str(valor))
        print(" ".join(valores))
