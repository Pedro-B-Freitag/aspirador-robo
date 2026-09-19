import random
import heapq

from agentes import agenteObjetivo, agenteReativoSimples


class Robo:
    TAMANHO = 18
    MODO_SIMPLES = "simples"
    MODO_OBJETIVO = "objetivo"

    def __init__(self, quarto, modo, posicoes_sujas=None):
        if modo not in (self.MODO_SIMPLES, self.MODO_OBJETIVO):
            raise ValueError("O modo deve ser 'simples' ou 'objetivo'.")

        self.linha = random.randrange(quarto.TAMANHO)
        self.coluna = random.randrange(quarto.TAMANHO)
        self.modo = modo
        self.posicoes_sujas = list(posicoes_sujas or self._posicoes_sujas(quarto))
        self.caminho_objetivo = self._montar_caminho(quarto)
        self.indice_caminho = self.caminho_objetivo.index((self.linha, self.coluna))
        self.sentido = self._sentido_inicial(quarto)
        self.fase = self._fase_inicial(quarto)
        self.pontos = 0
        self.visitados = {(self.linha, self.coluna)}
        self.rota_objetivo = []
        self.desenho = None

    def _fase_inicial(self, quarto):
        return "varrer" if self.linha == 0 else "subir"

    def _sentido_inicial(self, quarto):
        return "esquerda" if self.coluna == quarto.TAMANHO - 1 else "direita"

    def _montar_caminho(self, quarto):
        caminho = []
        for linha in range(quarto.TAMANHO):
            colunas = list(range(quarto.TAMANHO))
            if linha % 2 == 1:
                colunas.reverse()
            caminho.extend((linha, coluna) for coluna in colunas)
        return caminho

    def andar(self, quarto):
        if self.modo == self.MODO_OBJETIVO:
            if not self.posicoes_sujas:
                return False

            if not self.rota_objetivo:
                self.rota_objetivo = self._melhor_rota_para_sujeira(quarto)
            if not self.rota_objetivo:
                return False

            proxima_posicao = self.rota_objetivo.pop(0)
            self._mover_um_passo(*proxima_posicao)
            self.pontos += 1
            return True

        if self.fase == "subir" and self.linha == 0:
            self.fase = "varrer"
            self.sentido = self._sentido_inicial(quarto)

        percepcao = {
            "posicao": (self.linha + 1, self.coluna + 1),
            "estado": "sujo" if quarto.matriz[self.linha][self.coluna] == quarto.SUJO else "limpo",
            "paredes": {
                "acima": self.linha == 0,
                "abaixo": self.linha == quarto.TAMANHO - 1,
                "esquerda": self.coluna == 0,
                "direita": self.coluna == quarto.TAMANHO - 1,
            },
            "sentido": self.sentido,
            "fase": self.fase,
        }
        if self.modo == self.MODO_OBJETIVO:
            acao = agenteObjetivo(percepcao, checkObj(quarto))
        else:
            acao = agenteReativoSimples(percepcao)

        vizinhas = self._vizinhas(quarto)
        posicoes_nao_visitadas = [
            posicao for posicao in vizinhas if posicao not in self.visitados
        ]
        deslocamentos = {
            "acima": (-1, 0),
            "abaixo": (1, 0),
            "esquerda": (0, -1),
            "direita": (0, 1),
        }
        if posicoes_nao_visitadas:
            deslocamento_linha, deslocamento_coluna = deslocamentos.get(acao, (0, 0))
            destino_da_acao = (
                self.linha + deslocamento_linha,
                self.coluna + deslocamento_coluna,
            )
            if destino_da_acao not in posicoes_nao_visitadas:
                alvo = posicoes_nao_visitadas[0]
                if alvo[0] != self.linha:
                    acao = "abaixo" if alvo[0] > self.linha else "acima"
                else:
                    acao = "direita" if alvo[1] > self.coluna else "esquerda"
        elif len(self.visitados) < quarto.TAMANHO ** 2:
            posicoes_restantes = [
                (linha, coluna)
                for linha in range(quarto.TAMANHO)
                for coluna in range(quarto.TAMANHO)
                if (linha, coluna) not in self.visitados
            ]
            alvo = min(
                posicoes_restantes,
                key=lambda posicao: abs(posicao[0] - self.linha)
                + abs(posicao[1] - self.coluna),
            )
            if alvo[0] != self.linha:
                acao = "abaixo" if alvo[0] > self.linha else "acima"
            else:
                acao = "direita" if alvo[1] > self.coluna else "esquerda"

        if acao == "NoOp" or acao == "aspirar":
            return False

        deslocamento_linha, deslocamento_coluna = deslocamentos[acao]
        nova_linha = self.linha + deslocamento_linha
        nova_coluna = self.coluna + deslocamento_coluna
        if 0 <= nova_linha < quarto.TAMANHO and 0 <= nova_coluna < quarto.TAMANHO:
            self._mover_um_passo(nova_linha, nova_coluna)
            if acao in ("abaixo", "acima"):
                self.sentido = "esquerda" if self.sentido == "direita" else "direita"
            self.pontos += 1
        return True

    def _melhor_rota_para_sujeira(self, quarto):
        melhor_rota = []
        menor_custo = None
        origem = (self.linha, self.coluna)
        for sujeira in self.posicoes_sujas:
            rota = self._dijkstra(quarto, origem, sujeira)
            if rota and (menor_custo is None or len(rota) < menor_custo):
                melhor_rota = rota[1:]
                menor_custo = len(rota)
        return melhor_rota

    def _dijkstra(self, quarto, origem, destino):
        fila = [(0, origem)]
        distancias = {origem: 0}
        anteriores = {}

        while fila:
            distancia, atual = heapq.heappop(fila)
            if atual == destino:
                return self._reconstruir_rota(anteriores, origem, destino)
            if distancia != distancias[atual]:
                continue

            for vizinha in self._vizinhas(quarto, atual):
                nova_distancia = distancia + 1
                if nova_distancia < distancias.get(vizinha, float("inf")):
                    distancias[vizinha] = nova_distancia
                    anteriores[vizinha] = atual
                    heapq.heappush(fila, (nova_distancia, vizinha))
        return []

    def _reconstruir_rota(self, anteriores, origem, destino):
        rota = [destino]
        while rota[-1] != origem:
            rota.append(anteriores[rota[-1]])
        rota.reverse()
        return rota

    def _mover_um_passo(self, linha, coluna):
        if linha != self.linha:
            linha = self.linha + (1 if linha > self.linha else -1)
            coluna = self.coluna
        elif coluna != self.coluna:
            coluna = self.coluna + (1 if coluna > self.coluna else -1)
        self.mover_para(linha, coluna)

    def _vizinhas(self, quarto, posicao=None):
        if posicao is None:
            posicao = (self.linha, self.coluna)
        linha_atual, coluna_atual = posicao
        vizinhas = []
        for deslocamento_linha, deslocamento_coluna in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            linha = linha_atual + deslocamento_linha
            coluna = coluna_atual + deslocamento_coluna
            if 0 <= linha < quarto.TAMANHO and 0 <= coluna < quarto.TAMANHO:
                vizinhas.append((linha, coluna))
        return vizinhas

    def _posicoes_sujas(self, quarto):
        return [
            (linha, coluna)
            for linha in range(quarto.TAMANHO)
            for coluna in range(quarto.TAMANHO)
            if quarto.matriz[linha][coluna] == quarto.SUJO
        ]

    def tem_sujeira(self, quarto):
        return bool(self._posicoes_sujas(quarto))

    def limpar_sujeira(self, quarto):
        if quarto.matriz[self.linha][self.coluna] == quarto.SUJO:
            quarto.matriz[self.linha][self.coluna] = quarto.LIMPO
            if (self.linha, self.coluna) in self.posicoes_sujas:
                self.posicoes_sujas.remove((self.linha, self.coluna))
            self.rota_objetivo = []
            return True
        return False

    def mover_para(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
        self.visitados.add((linha, coluna))

    def desenhar(self, eixos, cor, deslocamento=0):
        self.deslocamento_visual = deslocamento
        self.desenho, = eixos.plot(
            [self.coluna + deslocamento],
            [self.linha + deslocamento],
            marker="o",
            color=tuple(valor / 255 for valor in cor),
            markersize=self.TAMANHO,
        )
        return self.desenho

    def atualizar_desenho(self):
        self.desenho.set_data(
            [self.coluna + self.deslocamento_visual],
            [self.linha + self.deslocamento_visual],
        )
        return self.desenho
