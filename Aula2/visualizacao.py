import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from quarto import Quarto
from robo import Robo

DESLOCAMENTO_GRADE = 0.5
DESLOCAMENTO_VISUAL = 1
VELOCIDADE_ROBO = 1000
LIMITE_INTERACOES_SIMPLES = 30
COR_QUARTO = {
    Quarto.LIMPO:  (255, 255, 255), # limpo
    Quarto.SUJO:   (139, 94, 52),   # sujo - marrom
}
COR_PAREDE = (74, 74, 74)

COR_ROBO = {
    "cor": (0, 191, 255),
}


def montar_imagem(matriz):
    tamanho = len(matriz)
    imagem = [[COR_PAREDE] * (tamanho + 2)]
    for linha in matriz:
        linha_de_COR_QUARTO = [COR_PAREDE]
        for valor in linha:
            linha_de_COR_QUARTO.append(COR_QUARTO[valor])
        linha_de_COR_QUARTO.append(COR_PAREDE)
        imagem.append(linha_de_COR_QUARTO)
    imagem.append([COR_PAREDE] * (tamanho + 2))
    return imagem


def desenhar_quarto(quarto: Quarto, modo):
    posicoes_sujas = [
        (linha, coluna)
        for linha in range(quarto.TAMANHO)
        for coluna in range(quarto.TAMANHO)
        if quarto.matriz[linha][coluna] == quarto.SUJO
    ]
    robo = Robo(quarto, modo, posicoes_sujas)
    imagem = montar_imagem(quarto.matriz)

    eixos = plt.gca()
    imagem_quarto = eixos.imshow(imagem)

    tamanho = quarto.TAMANHO + 2
    eixos.set_xticks([x - DESLOCAMENTO_GRADE for x in range(tamanho + 1)], minor=True)
    eixos.set_yticks([y - DESLOCAMENTO_GRADE for y in range(tamanho + 1)], minor=True)
    eixos.grid(which="minor", color="black", linewidth=1)
    eixos.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)

    robo.desenhar(eixos, COR_ROBO["cor"], DESLOCAMENTO_VISUAL)

    def atualizar(numero_interacao):
        limpou_sujeira = robo.limpar_sujeira(quarto)
        if limpou_sujeira:
            imagem_quarto.set_data(montar_imagem(quarto.matriz))
            print("Sujeira limpa:", (robo.linha, robo.coluna))

        if robo.modo == Robo.MODO_OBJETIVO and not robo.tem_sujeira(quarto):
            print("Quarto limpo!")
            print("Pontos:", robo.pontos)
            animacao.event_source.stop()
            return imagem_quarto, robo.atualizar_desenho()

        if limpou_sujeira:
            if (
                robo.modo == Robo.MODO_SIMPLES
                and numero_interacao == LIMITE_INTERACOES_SIMPLES - 1
            ):
                print("Interacoes encerradas.")
                print("Pontos:", robo.pontos)
            return imagem_quarto, robo.atualizar_desenho()

        robo.andar(quarto)

        if (
            robo.modo == Robo.MODO_SIMPLES
            and numero_interacao == LIMITE_INTERACOES_SIMPLES - 1
        ):
            print("Interacoes encerradas.")
            print("Pontos:", robo.pontos)

        return imagem_quarto, robo.atualizar_desenho()

    animacao = FuncAnimation(
        eixos.figure,
        atualizar,
        frames=LIMITE_INTERACOES_SIMPLES if robo.modo == Robo.MODO_SIMPLES else None,
        interval=VELOCIDADE_ROBO,
        repeat=False,
        blit=False,
        cache_frame_data=False,
    )

    plt.show()
