ACOES_MOVIMENTO = ("acima", "abaixo", "esquerda", "direita")
ACOES = ACOES_MOVIMENTO + ("aspirar",)
ACOES_OBJETIVO = ACOES + ("NoOp",)


def funcaoMapear(percepcao):
    paredes = percepcao["paredes"]
    sentido = percepcao.get("sentido", "direita")
    fase = percepcao.get("fase", "varrer")

    if fase == "subir":
        return "acima"

    lado_bloqueado = paredes[sentido]
    if lado_bloqueado and not paredes["abaixo"]:
        return "abaixo"
    if sentido == "direita" and not paredes["direita"]:
        return "direita"
    if sentido == "esquerda" and not paredes["esquerda"]:
        return "esquerda"
    if lado_bloqueado and not paredes["acima"]:
        return "acima"
    if not paredes["abaixo"]:
        return "abaixo"
    return "NoOp"


def agenteReativoSimples(percepcao):
    if percepcao["estado"] == "sujo":
        return "aspirar"
    return funcaoMapear(percepcao)


def checkObj(sala):
    matriz = sala.matriz if hasattr(sala, "matriz") else sala
    return int(any(2 in linha for linha in matriz))


def agenteObjetivo(percepcao, objObtido):
    if not objObtido:
        return "NoOp"
    if percepcao["estado"] == "sujo":
        return "aspirar"
    return funcaoMapear(percepcao)
