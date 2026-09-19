import quarto

PRIMEIRA = 1


def ultima():
    return quarto.TAMANHO - 2


def funcaoMapear(posicao):
    linha, coluna = posicao

    if linha == PRIMEIRA and coluna < ultima():
        return "direita"

    if coluna == PRIMEIRA:
        return "acima"

    if linha == ultima():
        return "esquerda"

    if linha % 2 == 0:
        if coluna > PRIMEIRA + 1:
            return "esquerda"
        return "abaixo"

    if coluna < ultima():
        return "direita"

    return "abaixo"


def agenteReativoSimples(percepcao):
    posicao, sujo = percepcao

    if sujo:
        return "aspirar"

    return funcaoMapear(posicao)

