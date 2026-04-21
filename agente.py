import random

PARADO = 0
DIREITA = 1
PULAR = 2
DIREITA_PULAR = 3

ACOES_VALIDAS = [PARADO, DIREITA, PULAR, DIREITA_PULAR]


def criar_gene():
    return random.choice(ACOES_VALIDAS)


def criar_cromossomo(tamanho_cromossomo):
    return [criar_gene() for _ in range(tamanho_cromossomo)]


def criar_individuo(tamanho_cromossomo):
    return criar_cromossomo(tamanho_cromossomo)


def criar_populacao(tamanho_populacao, tamanho_cromossomo):
    return [criar_individuo(tamanho_cromossomo) for _ in range(tamanho_populacao)]


def descrever_acao(acao):
    mapa = {
        PARADO: "PARADO",
        DIREITA: "DIREITA",
        PULAR: "PULAR",
        DIREITA_PULAR: "DIREITA_PULAR",
    }
    return mapa.get(acao, "DESCONHECIDA")


def descrever_cromossomo(cromossomo):
    return [descrever_acao(gene) for gene in cromossomo]