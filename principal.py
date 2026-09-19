import matplotlib.pyplot as plt

import agente
import ambiente
import visualizacao

# DEFINE QUAL AGENTE UTILIZAR
AGENTE = "objetivo"

PAUSA = 0.7


def decidir(sala, posicao):
    if AGENTE == "objetivo":
        percepcao = ambiente.perceber_com_sujeiras(sala, posicao)
        return agente.agenteObjetivo(percepcao, ambiente.checkObj(sala))

    percepcao = ambiente.perceber(sala, posicao)
    return agente.agenteReativoSimples(percepcao)


if __name__ == "__main__":
    sala = ambiente.gerar_sala()

    if AGENTE == "objetivo":
        posicao = (1, 1)
    else:
        posicao = ambiente.sortear_posicao()

    ambiente.exibir(sala, posicao)

    figura, ax = plt.subplots()
    visualizacao.desenhar(ax, sala, posicao, "inicio")
    plt.pause(PAUSA)

    pontos = 0
    while True:
        acao = decidir(sala, posicao)

        if acao == "NoOp":
            print(f"NoOp - sala limpa em {pontos} pontos")
            visualizacao.desenhar(ax, sala, posicao, f"sala limpa - {pontos} pontos")
            break

        if acao == "aspirar":
            ambiente.aspirar(sala, posicao)
        else:
            posicao = ambiente.mover(sala, posicao, acao)

        pontos += 1
        print(f"Pontos: {pontos}, Acao: {acao}, Posicao: {posicao}")

        visualizacao.desenhar(ax, sala, posicao, f"{pontos} pontos - {acao}")
        plt.pause(PAUSA)

    plt.show()
