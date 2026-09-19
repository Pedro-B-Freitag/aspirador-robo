import ambiente

PRIMEIRA = 1


def ultima():
    return ambiente.TAMANHO - 2


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


def agenteObjetivo(percepcao, objObtido):
    if objObtido == 0:
        return "NoOp"

    posicao, sujo, sujeiras = percepcao

    if sujo:
        return "aspirar"

    linha, coluna = posicao
    alvo_linha, alvo_coluna = sujeiras[0]

    if alvo_linha < linha:
        return "acima"

    if alvo_linha > linha:
        return "abaixo"

    if alvo_coluna < coluna:
        return "esquerda"

    return "direita"

