import matplotlib.pyplot as plt

import ambiente

CORES = {
    ambiente.LIMPO: (255, 255, 255),
    ambiente.PAREDE: (74, 74, 74),
    ambiente.SUJO: (139, 94, 52),
}

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

    ax.set_xticks([x - 0.5 for x in range(ambiente.TAMANHO + 1)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(ambiente.TAMANHO + 1)], minor=True)
    ax.grid(which="minor", color="black", linewidth=1)
    ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)
    ax.set_title(titulo)
