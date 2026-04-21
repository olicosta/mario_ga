import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt


def garantir_pasta_resultados():
    pasta = "resultados"
    os.makedirs(pasta, exist_ok=True)
    return pasta


def salvar_csv(historico_melhor, historico_medio, historico_pior):
    pasta = garantir_pasta_resultados()
    caminho = os.path.join(pasta, "historico_geracoes.csv")

    with open(caminho, mode="w", newline="", encoding="utf-8") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(["geracao", "melhor_fitness", "fitness_medio", "pior_fitness"])

        for i in range(len(historico_melhor)):
            writer.writerow([
                i + 1,
                historico_melhor[i],
                historico_medio[i],
                historico_pior[i]
            ])

    return caminho


def salvar_resumo(resultado_ag, parametros):
    pasta = garantir_pasta_resultados()
    caminho = os.path.join(pasta, "resumo_execucao.txt")

    melhor_resultado = resultado_ag["melhor_resultado"]
    melhor_individuo = resultado_ag["melhor_individuo"]

    with open(caminho, mode="w", encoding="utf-8") as arquivo:
        arquivo.write("RESUMO DA EXECUÇÃO DO ALGORITMO GENÉTICO\n")
        arquivo.write("=" * 50 + "\n\n")
        arquivo.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")

        arquivo.write("PARÂMETROS UTILIZADOS\n")
        arquivo.write("-" * 25 + "\n")
        for chave, valor in parametros.items():
            arquivo.write(f"{chave}: {valor}\n")

        arquivo.write("\nMELHOR SOLUÇÃO ENCONTRADA\n")
        arquivo.write("-" * 25 + "\n")
        arquivo.write(f"Melhor fitness: {resultado_ag['melhor_fitness']}\n")
        arquivo.write(f"Posição final X: {melhor_resultado['x']}\n")
        arquivo.write(f"Posição final Y: {melhor_resultado['y']}\n")
        arquivo.write(f"Vivo: {melhor_resultado['vivo']}\n")
        arquivo.write(f"Venceu: {melhor_resultado['venceu']}\n")
        arquivo.write(f"Passos executados: {melhor_resultado['passos']}\n")
        arquivo.write(f"Cromossomo vencedor:\n{melhor_individuo}\n")

    return caminho


def salvar_grafico_fitness(historico_melhor, historico_medio, historico_pior):
    pasta = garantir_pasta_resultados()
    caminho = os.path.join(pasta, "grafico_evolucao_fitness.png")

    geracoes = list(range(1, len(historico_melhor) + 1))

    plt.figure(figsize=(12, 6))
    plt.plot(geracoes, historico_melhor, label="Melhor fitness")
    plt.plot(geracoes, historico_medio, label="Fitness médio")
    plt.plot(geracoes, historico_pior, label="Pior fitness")

    plt.xlabel("Geração")
    plt.ylabel("Fitness")
    plt.title("Evolução do fitness ao longo das gerações")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(caminho, dpi=200)
    plt.close()

    return caminho


def salvar_grafico_convergencia(historico_melhor):
    pasta = garantir_pasta_resultados()
    caminho = os.path.join(pasta, "grafico_convergencia_melhor.png")

    geracoes = list(range(1, len(historico_melhor) + 1))

    plt.figure(figsize=(12, 6))
    plt.plot(geracoes, historico_melhor, label="Melhor fitness")
    plt.xlabel("Geração")
    plt.ylabel("Melhor fitness")
    plt.title("Convergência do melhor indivíduo")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(caminho, dpi=200)
    plt.close()

    return caminho


def gerar_resultados(resultado_ag, parametros):
    caminho_csv = salvar_csv(
        resultado_ag["historico_melhor"],
        resultado_ag["historico_medio"],
        resultado_ag["historico_pior"]
    )

    caminho_resumo = salvar_resumo(resultado_ag, parametros)

    caminho_grafico_fitness = salvar_grafico_fitness(
        resultado_ag["historico_melhor"],
        resultado_ag["historico_medio"],
        resultado_ag["historico_pior"]
    )

    caminho_grafico_convergencia = salvar_grafico_convergencia(
        resultado_ag["historico_melhor"]
    )

    return {
        "csv": caminho_csv,
        "resumo": caminho_resumo,
        "grafico_fitness": caminho_grafico_fitness,
        "grafico_convergencia": caminho_grafico_convergencia,
    }