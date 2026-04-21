import random
from agente import criar_populacao


def avaliar_populacao(populacao, ambiente):
    populacao_avaliada = []

    for individuo in populacao:
        fitness, resultado = ambiente.avaliar_individuo(individuo)
        populacao_avaliada.append((individuo, fitness, resultado))

    return populacao_avaliada


def selecao_torneio(populacao_avaliada, tamanho_torneio=3):
    candidatos = random.sample(populacao_avaliada, tamanho_torneio)
    candidatos.sort(key=lambda item: item[1], reverse=True)
    return candidatos[0][0]


def crossover_um_ponto(pai1, pai2):
    if len(pai1) != len(pai2):
        raise ValueError("Os pais precisam ter o mesmo tamanho.")

    if len(pai1) < 2:
        return pai1[:], pai2[:]

    ponto = random.randint(1, len(pai1) - 1)

    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]

    return filho1, filho2


def mutacao(individuo, taxa_mutacao=0.08):
    novo_individuo = individuo[:]

    for i in range(len(novo_individuo)):
        if random.random() < taxa_mutacao:
            novo_individuo[i] = random.randint(0, 3)

    return novo_individuo


def gerar_nova_populacao(
    populacao_avaliada,
    tamanho_populacao,
    elitismo=2,
    taxa_mutacao=0.08,
    tamanho_torneio=3,
):
    populacao_ordenada = sorted(populacao_avaliada, key=lambda item: item[1], reverse=True)

    nova_populacao = []

    for i in range(elitismo):
        nova_populacao.append(populacao_ordenada[i][0][:])

    while len(nova_populacao) < tamanho_populacao:
        pai1 = selecao_torneio(populacao_ordenada, tamanho_torneio)
        pai2 = selecao_torneio(populacao_ordenada, tamanho_torneio)

        filho1, filho2 = crossover_um_ponto(pai1, pai2)

        filho1 = mutacao(filho1, taxa_mutacao)
        filho2 = mutacao(filho2, taxa_mutacao)

        nova_populacao.append(filho1)

        if len(nova_populacao) < tamanho_populacao:
            nova_populacao.append(filho2)

    return nova_populacao


def executar_algoritmo_genetico(
    ambiente,
    tamanho_populacao=80,
    tamanho_cromossomo=90,
    geracoes=100,
    elitismo=2,
    taxa_mutacao=0.08,
    tamanho_torneio=3,
):
    populacao = criar_populacao(tamanho_populacao, tamanho_cromossomo)

    historico_melhor = []
    historico_medio = []
    historico_pior = []

    melhor_individuo_global = None
    melhor_fitness_global = float("-inf")
    melhor_resultado_global = None

    for geracao in range(geracoes):
        populacao_avaliada = avaliar_populacao(populacao, ambiente)

        melhor_da_geracao = max(populacao_avaliada, key=lambda item: item[1])
        pior_da_geracao = min(populacao_avaliada, key=lambda item: item[1])
        media_fitness = sum(item[1] for item in populacao_avaliada) / len(populacao_avaliada)

        historico_melhor.append(melhor_da_geracao[1])
        historico_medio.append(media_fitness)
        historico_pior.append(pior_da_geracao[1])

        if melhor_da_geracao[1] > melhor_fitness_global:
            melhor_individuo_global = melhor_da_geracao[0][:]
            melhor_fitness_global = melhor_da_geracao[1]
            melhor_resultado_global = melhor_da_geracao[2]

        print(
            f"Geração {geracao + 1:03d} | "
            f"Melhor: {melhor_da_geracao[1]:.2f} | "
            f"Médio: {media_fitness:.2f} | "
            f"Pior: {pior_da_geracao[1]:.2f} | "
            f"X melhor: {melhor_da_geracao[2]['x']} | "
            f"Venceu: {melhor_da_geracao[2]['venceu']}"
        )

        populacao = gerar_nova_populacao(
            populacao_avaliada=populacao_avaliada,
            tamanho_populacao=tamanho_populacao,
            elitismo=elitismo,
            taxa_mutacao=taxa_mutacao,
            tamanho_torneio=tamanho_torneio,
        )

    return {
        "melhor_individuo": melhor_individuo_global,
        "melhor_fitness": melhor_fitness_global,
        "melhor_resultado": melhor_resultado_global,
        "historico_melhor": historico_melhor,
        "historico_medio": historico_medio,
        "historico_pior": historico_pior,
    }