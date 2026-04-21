import pygame

LARGURA_JANELA = 1400
ALTURA_JANELA = 500
TAMANHO_BLOCO = 40

# Paleta inspirada em jogo retrô
COR_CEU = (107, 140, 255)
COR_NUVEM = (255, 255, 255)
COR_MONTANHA = (80, 180, 90)
COR_MONTANHA_SOMBRA = (60, 150, 70)

COR_CHAO_TOPO = (210, 150, 70)
COR_CHAO_CORPO = (170, 100, 40)
COR_CHAO_BORDA = (120, 70, 25)

COR_BURACO = (20, 20, 20)

COR_CANO = (20, 160, 20)
COR_CANO_BORDA = (10, 100, 10)

COR_BANDEIRA = (30, 200, 60)
COR_MASTRO = (230, 230, 230)

COR_TEXTO = (255, 255, 255)
COR_PAINEL = (0, 0, 0)

COR_MARIO_CHAPEU = (220, 30, 30)
COR_MARIO_ROUPA = (210, 40, 40)
COR_MARIO_PELE = (255, 210, 170)
COR_MARIO_CALCA = (40, 70, 220)
COR_MARIO_SAPATO = (80, 40, 20)


def visualizar_execucao(ambiente, acoes, fps=10):
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
    pygame.display.set_caption("Mario com Algoritmo Genético")
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont("arial", 24, bold=True)
    fonte_grande = pygame.font.SysFont("arial", 32, bold=True)

    ambiente.reset()

    indice_acao = 0
    rodando = True
    terminou = False
    mensagem_final = ""

    while rodando:
        relogio.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        if not terminou:
            if indice_acao < len(acoes):
                ambiente.aplicar_acao(acoes[indice_acao])
                indice_acao += 1
            else:
                terminou = True
                mensagem_final = "Sequência finalizada - feche a janela"

            if not ambiente.vivo:
                terminou = True
                mensagem_final = "Mario morreu - feche a janela"

            if ambiente.venceu:
                terminou = True
                mensagem_final = "Fase concluída! - feche a janela"

        camera_x = calcular_camera_x(ambiente)

        desenhar_fundo(tela)
        desenhar_fase(tela, ambiente, camera_x)
        desenhar_bandeira(tela, ambiente, camera_x)
        desenhar_mario(tela, ambiente, camera_x)
        desenhar_hud(tela, fonte, fonte_grande, ambiente, indice_acao, len(acoes), mensagem_final)

        pygame.display.flip()

    pygame.quit()


def calcular_camera_x(ambiente):
    mundo_x = ambiente.mario_x * TAMANHO_BLOCO
    centro_tela = LARGURA_JANELA // 2
    camera_x = mundo_x - centro_tela
    return max(0, camera_x)


def desenhar_fundo(tela):
    tela.fill(COR_CEU)

    # nuvens
    nuvens = [
        (120, 70), (380, 95), (680, 60), (980, 90), (1220, 70)
    ]
    for x, y in nuvens:
        desenhar_nuvem(tela, x, y)

    # montanhas
    montanhas = [
        (80, 380, 220, 120),
        (340, 370, 260, 130),
        (700, 390, 220, 110),
        (1030, 365, 280, 135),
    ]
    for x, base_y, largura, altura in montanhas:
        desenhar_montanha(tela, x, base_y, largura, altura)


def desenhar_nuvem(tela, x, y):
    pygame.draw.circle(tela, COR_NUVEM, (x, y), 22)
    pygame.draw.circle(tela, COR_NUVEM, (x + 24, y - 8), 26)
    pygame.draw.circle(tela, COR_NUVEM, (x + 52, y), 22)
    pygame.draw.rect(tela, COR_NUVEM, (x, y - 10, 52, 24))


def desenhar_montanha(tela, x, base_y, largura, altura):
    pontos = [
        (x, base_y),
        (x + largura // 2, base_y - altura),
        (x + largura, base_y)
    ]
    pygame.draw.polygon(tela, COR_MONTANHA, pontos)

    sombra = [
        (x + largura // 2, base_y - altura),
        (x + largura, base_y),
        (x + largura // 2 + 40, base_y)
    ]
    pygame.draw.polygon(tela, COR_MONTANHA_SOMBRA, sombra)


def desenhar_fase(tela, ambiente, camera_x):
    offset_x = 0
    offset_y = 180

    # chão
    for x in range(ambiente.largura):
        tela_x = offset_x + x * TAMANHO_BLOCO - camera_x
        tela_y = offset_y + ambiente.chao_y * TAMANHO_BLOCO

        if tela_x > LARGURA_JANELA or tela_x + TAMANHO_BLOCO < 0:
            continue

        if x in ambiente.buracos:
            pygame.draw.rect(
                tela,
                COR_BURACO,
                (tela_x, tela_y, TAMANHO_BLOCO, TAMANHO_BLOCO * 3)
            )
        else:
            desenhar_bloco_chao(tela, tela_x, tela_y)

    # obstáculos viram canos
    for x in ambiente.obstaculos:
        tela_x = offset_x + x * TAMANHO_BLOCO - camera_x
        tela_y = offset_y + (ambiente.chao_y - 1) * TAMANHO_BLOCO

        if tela_x > LARGURA_JANELA or tela_x + TAMANHO_BLOCO < 0:
            continue

        desenhar_cano(tela, tela_x, tela_y)


def desenhar_bloco_chao(tela, x, y):
    pygame.draw.rect(tela, COR_CHAO_CORPO, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
    pygame.draw.rect(tela, COR_CHAO_TOPO, (x, y, TAMANHO_BLOCO, 10))
    pygame.draw.rect(tela, COR_CHAO_BORDA, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO), 2)

    # detalhes internos
    pygame.draw.line(tela, COR_CHAO_BORDA, (x + 10, y + 10), (x + 30, y + 10), 2)
    pygame.draw.line(tela, COR_CHAO_BORDA, (x + 8, y + 26), (x + 16, y + 18), 2)
    pygame.draw.line(tela, COR_CHAO_BORDA, (x + 24, y + 28), (x + 32, y + 20), 2)


def desenhar_cano(tela, x, y):
    # topo do cano
    pygame.draw.rect(tela, COR_CANO, (x - 4, y, TAMANHO_BLOCO + 8, 12))
    pygame.draw.rect(tela, COR_CANO_BORDA, (x - 4, y, TAMANHO_BLOCO + 8, 12), 2)

    # corpo
    pygame.draw.rect(tela, COR_CANO, (x, y + 12, TAMANHO_BLOCO, TAMANHO_BLOCO - 12))
    pygame.draw.rect(tela, COR_CANO_BORDA, (x, y + 12, TAMANHO_BLOCO, TAMANHO_BLOCO - 12), 2)

    # brilho
    pygame.draw.line(tela, (120, 240, 120), (x + 8, y + 14), (x + 8, y + TAMANHO_BLOCO - 4), 3)


def desenhar_bandeira(tela, ambiente, camera_x):
    offset_x = 0
    offset_y = 180

    base_x = offset_x + ambiente.fim_x * TAMANHO_BLOCO - camera_x
    base_y = offset_y + (ambiente.chao_y - 1) * TAMANHO_BLOCO

    pygame.draw.rect(tela, COR_MASTRO, (base_x + 12, base_y - 120, 6, 120))
    pygame.draw.circle(tela, COR_MASTRO, (base_x + 15, base_y - 120), 6)
    pygame.draw.polygon(
        tela,
        COR_BANDEIRA,
        [(base_x + 18, base_y - 110), (base_x + 55, base_y - 100), (base_x + 18, base_y - 88)]
    )


def desenhar_mario(tela, ambiente, camera_x):
    offset_x = 0
    offset_y = 180

    x = offset_x + ambiente.mario_x * TAMANHO_BLOCO - camera_x
    y = offset_y + ambiente.mario_y * TAMANHO_BLOCO

    # sapatos
    pygame.draw.rect(tela, COR_MARIO_SAPATO, (x + 6, y + 34, 10, 6))
    pygame.draw.rect(tela, COR_MARIO_SAPATO, (x + 20, y + 34, 10, 6))

    # pernas/calça
    pygame.draw.rect(tela, COR_MARIO_CALCA, (x + 8, y + 24, 18, 12))

    # corpo
    pygame.draw.rect(tela, COR_MARIO_ROUPA, (x + 6, y + 12, 22, 14))

    # braços
    pygame.draw.rect(tela, COR_MARIO_PELE, (x + 2, y + 14, 6, 10))
    pygame.draw.rect(tela, COR_MARIO_PELE, (x + 28, y + 14, 6, 10))

    # rosto
    pygame.draw.rect(tela, COR_MARIO_PELE, (x + 10, y + 4, 14, 10))

    # chapéu
    pygame.draw.rect(tela, COR_MARIO_CHAPEU, (x + 8, y, 18, 6))
    pygame.draw.rect(tela, COR_MARIO_CHAPEU, (x + 6, y + 5, 22, 4))

    # olho
    pygame.draw.rect(tela, (0, 0, 0), (x + 20, y + 7, 2, 2))


def desenhar_hud(tela, fonte, fonte_grande, ambiente, indice_acao, total_acoes, mensagem_final):
    painel = pygame.Surface((LARGURA_JANELA, 55))
    painel.set_alpha(150)
    painel.fill(COR_PAINEL)
    tela.blit(painel, (0, 0))

    textos = [
        f"X: {ambiente.mario_x}",
        f"Y: {ambiente.mario_y}",
        f"Passos: {ambiente.passos}",
        f"Ação: {indice_acao}/{total_acoes}",
        f"Vivo: {ambiente.vivo}",
        f"Venceu: {ambiente.venceu}",
    ]

    x = 20
    for texto in textos:
        superficie = fonte.render(texto, True, COR_TEXTO)
        tela.blit(superficie, (x, 15))
        x += 150

    if mensagem_final:
        superficie = fonte_grande.render(mensagem_final, True, COR_TEXTO)
        tela.blit(superficie, (820, 12))