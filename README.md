Segue um passo a passo para rodar o projeto do zero no seu Windows.

1. Abrir a pasta do projeto no terminal

No PowerShell, entre na pasta:

cd D:\Users\User\mario_ga

Para conferir os arquivos:

dir

Você deve ver algo como:

main.py
ambiente.py
agente.py
ag.py
visualizacao.py
resultados.py
2. Confirmar se o Python está funcionando

Rode:

py --version

Se aparecer a versão do Python, está certo.

3. Instalar as bibliotecas necessárias

Instale o que o projeto usa:

py -m pip install pygame matplotlib
4. Limpar cache antigo do Python

Isso evita erro com arquivos salvos anteriormente:

Remove-Item -Recurse -Force .\__pycache__ -ErrorAction SilentlyContinue

Se quiser limpar caches em subpastas também:

Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
5. Testar se o ambiente principal importa corretamente

Antes de rodar tudo, teste:

py -c "from ambiente import AmbienteMario; print(AmbienteMario)"

O esperado é aparecer algo como:

<class 'ambiente.AmbienteMario'>
6. Rodar o projeto

Agora execute:

py main.py
7. O que vai acontecer

Quando você rodar, o fluxo será este:

Etapa A

O algoritmo genético começa a treinar e mostra no terminal linhas como:

Geração 001 | Melhor: ... | Médio: ... | Pior: ... | X melhor: ... | Venceu: ...
Etapa B

No final, ele mostra:

melhor fitness encontrado
resultado final
cromossomo vencedor
render em texto da fase
Etapa C

Depois ele cria a pasta:

resultados

e salva:

historico_geracoes.csv
resumo_execucao.txt
grafico_evolucao_fitness.png
grafico_convergencia_melhor.png
Etapa D

Por fim, abre a janela com a visualização do jogo.

8. Como abrir os resultados

Depois da execução, entre na pasta:

cd .\resultados
dir

Para abrir o gráfico no Windows Explorer:

start grafico_evolucao_fitness.png

ou:

start grafico_convergencia_melhor.png

Para abrir o resumo:

notepad resumo_execucao.txt

Para abrir o CSV:

start historico_geracoes.csv
9. Como rodar de novo

Sempre que quiser executar novamente:

cd D:\Users\User\mario_ga
py main.py

Cada execução é um novo experimento do zero.

10. Se der erro
Erro de import

Limpe cache e teste de novo:

Remove-Item -Recurse -Force .\__pycache__ -ErrorAction SilentlyContinue
py -c "from ambiente import AmbienteMario; print(AmbienteMario)"
pygame não encontrado

Instale novamente:

py -m pip install pygame
matplotlib não encontrado

Instale novamente:

py -m pip install matplotlib