from quarto import Quarto
from robo import Robo
from visualizacao import desenhar_quarto

#MODO_ROBO = Robo.MODO_OBJETIVO
MODO_ROBO = Robo.MODO_SIMPLES

def main():
    quarto = Quarto()
    quarto.exibir()
    desenhar_quarto(quarto, MODO_ROBO)


if __name__ == "__main__":
    main()
