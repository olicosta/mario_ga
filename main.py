from ambiente import AmbienteMario
from ag import executar_algoritmo_genetico
from visualizacao import visualizar_execucao
from resultados import gerar_resultados


def executar_projeto():
    ambiente = AmbienteMario()

    parametros = {
        "tamanho_populacao": 80,
        "tamanho_cromossomo": 90,
        "geracoes": 100,
        "elitismo": 2,
        "taxa_mutacao": 0.08,
        "tamanho_torneio": 3,
    }

    resultado_ag = executar_algoritmo_genetico(
        ambiente=ambiente,
        tamanho_populacao=parametros["tamanho_populacao"],
        tamanho_cromossomo=parametros["tamanho_cromossomo"],
        geracoes=parametros["geracoes"],
        elitismo=parametros["elitismo"],
        taxa_mutacao=parametros["taxa_mutacao"],
        tamanho_torneio=parametros["tamanho_torneio"],
    )

    print("\n=== MELHOR INDIVIDUO ENCONTRADO ===")
    print("Fitness:", resultado_ag["melhor_fitness"])
    print("Resultado:", resultado_ag["melhor_resultado"])
    print("Cromossomo:", resultado_ag["melhor_individuo"])

    print("\n=== ESTADO FINAL DO MELHOR INDIVIDUO ===")
    ambiente.simular(resultado_ag["melhor_individuo"])
    print(ambiente.render_texto())

    arquivos = gerar_resultados(resultado_ag, parametros)

    print("\n=== ARQUIVOS GERADOS ===")
    print("CSV:", arquivos["csv"])
    print("Resumo:", arquivos["resumo"])
    print("Gráfico fitness:", arquivos["grafico_fitness"])
    print("Gráfico convergência:", arquivos["grafico_convergencia"])

    print("\nAbrindo visualização...")
    visualizar_execucao(ambiente, resultado_ag["melhor_individuo"], fps=10)


if __name__ == "__main__":
    executar_projeto()