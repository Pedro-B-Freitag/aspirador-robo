import matplotlib.pyplot as plt

import quarto
import robo

AGENTE = "reativo"

CORES = {
    quarto.LIMPO: (255, 255, 255),
    quarto.PAREDE: (74, 74, 74),
    quarto.SUJO: (139, 94, 52),
}

PAUSA = 0.7
COR_AGENTE = "black"
RAIO_AGENTE = 0.32


def montar_imagem(sala):
    imagem = []
    for linha in sala:
        linha_de_cores = []
        for valor in linha:
            linha_de_cores.append(CORES[valor])
        imagem.append(linha_de_cores)
    return imagem


def desenhar(ax, sala, posicao, titulo):
    ax.clear()
    ax.imshow(montar_imagem(sala))

    linha, coluna = posicao
    ax.add_patch(plt.Circle((coluna, linha), RAIO_AGENTE, color=COR_AGENTE))

    ax.set_xticks([x - 0.5 for x in range(quarto.TAMANHO + 1)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(quarto.TAMANHO + 1)], minor=True)
    ax.grid(which="minor", color="black", linewidth=1)
    ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)
    ax.set_title(titulo)


if __name__ == "__main__":
    sala = quarto.gerar_sala()
    posicao = quarto.sortear_posicao()

    quarto.exibir(sala, posicao)

    figura, ax = plt.subplots()
    desenhar(ax, sala, posicao, "inicio")
    plt.pause(PAUSA)

    pontos = 0
    while True:
        percepcao = (posicao, quarto.esta_sujo(sala, posicao))

        acao = robo.agenteReativoSimples(percepcao)

        if acao == "aspirar":
            quarto.aspirar(sala, posicao)
            pontos += 1
        elif acao != "NoOp":
            posicao = quarto.mover(sala, posicao, acao)
            pontos += 1

        print(f"Pontos: {pontos}, Acao: {acao}, Posicao: {posicao}")

        desenhar(ax, sala, posicao, f"{pontos} pontos - {acao}")
        plt.pause(PAUSA)
